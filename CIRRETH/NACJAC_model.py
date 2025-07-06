import torch
import torch.nn as nn
import torch.nn.functional as F

class NACJAC_selfAttentionHead(nn.Module):
    def __init__(self, head_size, n_embed, block_size, device):
        super().__init__()
        self.key = nn.Linear(n_embed, head_size, bias=False)
        self.query = nn.Linear(n_embed, head_size, bias=False)
        self.value = nn.Linear(n_embed, head_size, bias=False)
        self.tril = torch.tril(torch.ones(block_size, block_size)).to(device=device)
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)
        q = self.query(x)
        wei = q @ k.transpose(-2,-1)/C**0.5
        wei = wei.masked_fill(self.tril[:T,:T] == 0, float('-inf'))
        wei = F.softmax(wei, dim = -1)
        wei = self.dropout(wei)
        v = self.value(x)
        return wei @ v
    
class NACJAC_MultiHeadAttention(nn.Module):
    def __init__(self, num_heads, head_size, n_embed, block_size, device):
        super().__init__()
        self.heads = nn.ModuleList([NACJAC_selfAttentionHead(head_size, n_embed, block_size, device)
                                    for _ in range(num_heads)])
        self.proj = nn.Linear(n_embed, n_embed)
        self.dropout = nn.Dropout(0.1)

    
    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim = -1)
        out = self.dropout(self.proj(out))
        return out
    
class NACJAC_FeedForward(nn.Module):
    def __init__(self, n_embed):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embed, 4 * n_embed),
            nn.ReLU(),
            nn.Linear(4 * n_embed, n_embed),
            nn.Dropout(0.1)
        )
    
    def forward(self, x):
        return self.net(x)

class NACJAC_Block(nn.Module):
    def __init__(self, n_embed, n_heads, block_size, device):
        super().__init__()
        head_size = n_embed // n_heads
        self.sa = NACJAC_MultiHeadAttention(n_heads, head_size, n_embed, block_size, device)
        self.ffwd = NACJAC_FeedForward(n_embed)
        self.ln1 = nn.LayerNorm(n_embed)
        self.ln2 = nn.LayerNorm(n_embed)

    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x
    
class NACJAC_LangModel(nn.Module):
    def __init__(self, config, vocab_size):
        super().__init__()
        self.config = config
        self.token_embedding_table = nn.Embedding(vocab_size, config.n_embed)
        self.position_embedding_table = nn.Embedding(config.block_size, config.n_embed)
        self.blocks = nn.Sequential(*[
            NACJAC_Block(config.n_embed, config.n_heads, config.block_size, config.device)
            for _ in range(config.n_layers)
        ])
        self.ln_f = nn.LayerNorm(config.n_embed)
        self.lm_head = nn.Linear(config.n_embed, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        tok_emb = self.token_embedding_table(idx)
        pos_emb = self.position_embedding_table(torch.arange(T, device=self.config.device))
        x = tok_emb + pos_emb
        x = self.blocks(x)
        x = self.ln_f(x)
        logits = self.lm_head(x)

        loss = None
        if targets is not None:
            logits = logits.view(B * T, -1)
            targets = targets.view(B * T)
            loss = F.cross_entropy(logits, targets)

        return logits, loss

    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.config.block_size:]
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :]
            probs = F.softmax(logits, dim=-1)
            next_idx = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, next_idx), dim=1)
        return idx

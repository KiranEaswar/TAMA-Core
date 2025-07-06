import os
import torch

class NACJAC_Tokeniser:
    def __init__(self,config):
        self.vocab_path = config.vocab_path
        self.stoi = {}
        self.itos = {}

        if os.path.exists(self.vocab_path):
            self._load_vocab()
        else:
            self._build_vocab(config.vocab_path)
            self._save_vocab()
        
    def _build_vocab(self, filepath):
        with open(filepath,'r',encoding = 'utf-8') as f:
            text = f.read()
        chars = sorted(list(set(text)))
        self.stoi = {ch:i for i,ch in enumerate(chars)}
        self.itos = {i:ch for i,ch in enumerate(chars)}
    
    def _save_vocab(self):
        torch.save((self.stoi, self.itos), self.vocab_path)
    def _load_vocab(self):
        self.stoi, self.itos = torch.load(self.vocab_path)
    
    def encode(self, s):
        return [self.stoi[c] for c in s]
    
    def decode(self, s):
        return ''.join([self.itos[i] for i in s])
    
    def vocab_size(self):
        return len(self.stoi)

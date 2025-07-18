import torch
from NACJAC_model import NACJAC_LangModel
from NACJAC_tokeniser import NACJAC_Tokeniser
from NACJAC_DataLoader import NACJAC_Dataloader

class NACJAC_FineTuner:
    def __init__(self, config):
        self.config = config
        self.tokenizer = NACJAC_Tokeniser(config)
        self.data_loader = NACJAC_Dataloader(config, self.tokenizer)

        self.model = NACJAC_LangModel(config, self.tokenizer.vocab_size()).to(config.device)
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=config.learning_rate)

        print("Loading pre-trained weights...")
        self.model.load_state_dict(torch.load(config.model_path, map_location=config.device))

    def fine_tune(self):
        print(f"Fine-tuning from: {self.config.model_path}")
        for step in range(self.config.max_iters):
            xb, yb = self.data_loader.get_batch('train')
            logits, loss = self.model(xb, yb)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            if step % self.config.eval_interval == 0:
                print(f"[Fine-Tune Step {step}] Loss: {loss.item():.4f}")

        torch.save(self.model.state_dict(), self.config.model_path)
        print(f"Updated model saved to {self.config.model_path}")

import torch
from NACJAC_configurator import NACJAC_Config
from NACJAC_tokeniser import NACJAC_Tokeniser

class NACJAC_Dataloader:
    def __init__(self, config: NACJAC_Config, tokeniser: NACJAC_Tokeniser):
        self.config = config
        self.tokeniser = tokeniser
        self.data = self._load_data()
        self.train_data, self.val_data = self._split_data()

    def _load_data(self):
        with open(self.config.data_path, 'r', encoding = 'utf-8') as f:
            text = f.read()
        encoded = self.tokeniser.encode(text)
        return torch.tensor(encoded, dtype = torch.long)
    def _split_data(self):
        n = int(0.8 * len(self.data))
        return self.data[:n], self.data[n:]
    
    def _get_batch(self, split = 'train'):
        data_ = self.train_data if split=='train' else self.val_data
        ix = torch.randint(len(data_) - self.config.block_size, (self.config.block_size,))
        x = torch.stack([data_[i:i+self.config.block_size] for i in ix])
        y = torch.stack([data_[i+1:i+self.config.block_size+1] for i in ix])
        return x.to(self.config.device), y.to(self.config.device)
        

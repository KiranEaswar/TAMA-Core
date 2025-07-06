import os
import re
import torch

#CIRRETH _ CONFIG
class NACJAC_Config:
    def __init__(self):
        self.base_model_name = "NACJAC_v1"
        self.base_vocab_name = "NACJAC_vocab_v1"
        self.finetune_loop = self._get_latest_model_version()
        
        self.model_path = f"{self.base_model_name}_{self.finetune_loop}.pt"
        self.vocab_path = f"{self.base_vocab_name}_0.pt"

        self.batch_size = 64
        self.block_size = 128
        self.max_iters = 10000
        self.eval_interval = 500
        self.learning_rate = 3e-4
        self.n_embed = 512
        self.n_heads = 8
        self.n_layers = 8
        self.current_datapath = "wiz_of_oz.txt"
        self.max_tokens = 300
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def _get_latest_model_version(self):
        files = os.listdir()
        pattern = re.compile(fr"{self.base_model_name}_(\d+)\.pt")
        versions = [int(match.group(1)) for file in files if (match := pattern.match(file))]
        return max(versions) if versions else 0

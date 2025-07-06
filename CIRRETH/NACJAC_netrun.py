import torch
from NACJAC_model import NACJAC_LangModel
from NACJAC_tokeniser import NACJAC_Tokeniser
from NACJAC_configurator import NACJAC_Config

class NACJAC_Generator:
    def __init__(self, config):
        self.config = config
        self.tokenizer = NACJAC_Tokeniser(config)
        self.vocab_size = self.tokenizer.vocab_size()
        self.model = NACJAC_LangModel(config, self.vocab_size).to(config.device)
        self.model.load_state_dict(torch.load(config.model_path, map_location=config.device))
        self.model.eval()

    def generate_text(self, prompt: str = "", max_tokens=None):
        if max_tokens is None:
            max_tokens = self.config.max_tokens
        idx = torch.tensor([self.tokenizer.encode(prompt)], dtype=torch.long).to(self.config.device)
        out = self.model.generate(idx, max_tokens)[0].tolist()
        return self.tokenizer.decode(out)


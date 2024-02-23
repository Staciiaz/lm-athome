import torch

from transformers import AutoModelForCausalLM, AutoTokenizer

from ..types.chat_completion import ConversationHistory
from ..utils import extract_assistant_output
from .chat_model import ChatModel


class Mistral(ChatModel):
    def __init__(self, model_id: str) -> None:
        self.device = "cuda"
        self.templates = ("[/INST] ", "</s>")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, device_map=self.device, torch_dtype=torch.bfloat16)

    def chat_completions(self, messages: ConversationHistory) -> str:
        encodeds = self.tokenizer.apply_chat_template(messages, return_tensors="pt")
        model_inputs = encodeds.to(self.device)
        generated_ids = self.model.generate(model_inputs, max_new_tokens=1000, do_sample=True, pad_token_id=self.tokenizer.eos_token_id)
        decoded = self.tokenizer.batch_decode(generated_ids)
        return extract_assistant_output(decoded[0], self.templates)

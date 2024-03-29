from transformers import BitsAndBytesConfig
import torch


def extract_assistant_output(output: str, templates: tuple[str]) -> str:
    return output[output.rindex(templates[0])+len(templates[0]):output.rindex(templates[1])].strip()


def get_quantization_config(dtype: str) -> tuple[torch.dtype, BitsAndBytesConfig]:
    dtype = dtype.lower()
    if dtype == "fp32":
        return torch.float32, None
    elif dtype == "bf16":
        return torch.bfloat16, None
    elif dtype == "fp16":
        return torch.float16, None
    elif dtype == "int8":
        return None, BitsAndBytesConfig(load_in_8bit=True)
    elif dtype == "int4":
        return None, BitsAndBytesConfig(load_in_4bit=True)
    elif dtype == "" or dtype is None:
        return None, None
    else:
        raise ValueError(f"Invalid dtype: {dtype}")
    

def get_device_config(device: str) -> str:
    device = device.lower()
    if device in ("cpu", "cuda", "mps"):
        return device
    elif device == "" or device is None:
        return "cpu"
    else:
        raise ValueError(f"Invalid device: {device}")

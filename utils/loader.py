import torch

from transformers import AutoTokenizer
from intel_extension_for_transformers.transformers import AutoModelForCausalLM, WeightOnlyQuantConfig

def ITREXLoader(model_name: str, trust_remote_code: bool = True):


    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=trust_remote_code)
    
    if model_name == 'Intel/neural-chat-7b-v1-1':
        model = AutoModelForCausalLM.from_pretrained(model_name, load_in_4bit=True)
    elif model_name == 'Intel/neural-chat-7b-v3-1':
          #model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)
          #config = WeightOnlyQuantConfig(compute_dtype="bf16", weight_dtype="int4")
          model = AutoModelForCausalLM.from_pretrained(model_name, load_in_4bit=True)


    return model, tokenizer
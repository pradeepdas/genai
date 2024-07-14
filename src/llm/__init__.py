import torch
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from llama_index.core.llms import LLM as BaseLLM
from llama_index.llms.openai import OpenAI
from llama_index.llms.huggingface import HuggingFaceLLM as HFLLMBase

class LLM(ABC):
    @abstractmethod
    def get_llm(self) -> BaseLLM:
        pass

class OpenAILLM(LLM):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_llm(self) -> BaseLLM:
        return OpenAI(api_key=self.api_key)

class HuggingFaceLLM(LLM):
    def __init__(self, 
                 model_name: str, 
                 tokenizer_name: str,
                 context_window: int = 8000,
                 max_new_tokens: int = 256,
                 generate_kwargs: Optional[Dict[str, Any]] = None,
                 model_kwargs: Optional[Dict[str, Any]] = None,
                 tokenizer_kwargs: Optional[Dict[str, Any]] = None):
        self.model_name = model_name
        self.tokenizer_name = tokenizer_name
        self.context_window = context_window
        self.max_new_tokens = max_new_tokens
        self.generate_kwargs = generate_kwargs or {"temperature": 0.1, "do_sample": True}
        self.model_kwargs = model_kwargs or {}
        self.tokenizer_kwargs = tokenizer_kwargs or {"max_length": 8000}

    def get_llm(self) -> BaseLLM:
        device = self._get_device()
        print(f"Using device: {device}")

        if device == "cuda":
            self.model_kwargs["torch_dtype"] = torch.float16
        elif device == "mps":
            self.model_kwargs["torch_dtype"] = torch.float32

        return HFLLMBase(
            context_window=self.context_window,
            max_new_tokens=self.max_new_tokens,
            generate_kwargs=self.generate_kwargs,
            tokenizer_name=self.tokenizer_name,
            model_name=self.model_name,
            device_map=device,
            tokenizer_kwargs=self.tokenizer_kwargs,
            model_kwargs=self.model_kwargs
        )

    def _get_device(self) -> str:
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            print("CUDA and MPS are not available. Using CPU instead.")
            return "cpu"

class LLMFactory:
    @staticmethod
    def get_llm(llm_type: str, **kwargs) -> LLM:
        if llm_type.lower() == "openai":
            api_key = kwargs.get('api_key')
            if not api_key:
                raise ValueError("API key is required for OpenAI LLM")
            return OpenAILLM(api_key)
        elif llm_type.lower() == "huggingface":
            model_name = kwargs.get('model_name')
            tokenizer_name = kwargs.get('tokenizer_name')
            if not model_name or not tokenizer_name:
                raise ValueError("Both model_name and tokenizer_name are required for HuggingFace LLM")
            return HuggingFaceLLM(
                model_name=model_name,
                tokenizer_name=tokenizer_name,
                context_window=kwargs.get('context_window', 8000),
                max_new_tokens=kwargs.get('max_new_tokens', 256),
                generate_kwargs=kwargs.get('generate_kwargs'),
                model_kwargs=kwargs.get('model_kwargs'),
                tokenizer_kwargs=kwargs.get('tokenizer_kwargs')
            )
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")
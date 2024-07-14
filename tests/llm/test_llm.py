import os
from dotenv import load_dotenv
from src.llm import LLMFactory

load_dotenv()  # This loads the variables from .env file

def test_llm(llm, query):
    llm_instance = llm.get_llm()
    response = llm_instance.complete(query)
    return response

def main():
    # Test OpenAI LLM
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_llm = LLMFactory.get_llm("openai", api_key=openai_api_key)
    
    # # Test HuggingFace LLM
    # hf_llm = LLMFactory.get_llm("huggingface", 
    #                             model_name="mistralai/Mistral-7B-Instruct-v0.1", 
    #                             tokenizer_name="mistralai/Mistral-7B-Instruct-v0.1")

    # Test query
    test_query = "What is the capital of France?"

    print("Testing OpenAI LLM:")
    openai_response = test_llm(openai_llm, test_query)
    print(f"OpenAI Response: {openai_response}")

    # print("\nTesting HuggingFace LLM:")
    # hf_response = test_llm(hf_llm, test_query)
    # print(f"HuggingFace Response: {hf_response}")

if __name__ == "__main__":
    main()
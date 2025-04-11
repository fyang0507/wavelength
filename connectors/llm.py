from openai import OpenAI
from anthropic import Anthropic
import os
from loguru import logger
from dotenv import load_dotenv

# Call the appropriate API based on the model name
def api_text_completion(model, system_prompt, user_message):
    """
    Create a completion using the appropriate AI API based on the model name.
    
    Args:
        model (str): The model name
        system_prompt (str): The system prompt
        user_message (str): The user message
        
    Returns:
        The API response
    """
    load_dotenv()
    logger.info(f"Using model: {model}")

    if model.startswith("claude"):
        # Call Anthropic API
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        return client.messages.create(
            model=model,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ],
            max_tokens=4096
        ).content[0].text
    elif model.startswith("gpt"):
        # Call OpenAI API
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        return client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.0
        ).choices[0].message.content
    else:
        raise ValueError(f"Invalid model: {model}")
    

# Main function for testing the API text completion
if __name__ == "__main__":
    
    # Test configuration
    test_models = [
        "gpt-4o-mini",
        "claude-3-5-haiku-20241022"
    ]
    
    system_prompt = "You are a helpful assistant. Summarize the following text in 3 bullet points."
    user_message = "Artificial intelligence is transforming industries across the global economy. Companies are using AI to automate tasks, gain insights from data, and create new products and services. However, the rapid advancement of AI also raises concerns about job displacement, privacy, and ethical considerations."
    
    print("\n=== LLM Connector Test ===\n")
    
    # Test each model
    for model in test_models:
        print(f"\nTesting model: {model}")
        try:
            response = api_text_completion(model, system_prompt, user_message)
            
            # Format and print the response based on the model type
            if model.startswith("gpt"):
                content = response.choices[0].message.content
            elif model.startswith("claude"):
                content = response.content
            
            print(f"\nResponse:\n{content}\n")
            print("-" * 50)
        except Exception as e:
            print(f"Error testing {model}: {e}")
    
    print("\nTest completed.")
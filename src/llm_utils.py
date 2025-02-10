import openai
import os

def query_llm(prompt, image=None):
    openai.api_key = os.getenv("AIPROXY_TOKEN")
    
    # Set API base if using a proxy
    openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    
    try:
        if image:
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",  # Use vision model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
        else:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )

        return response["choices"][0]["message"]["content"].strip()
    
    except openai.error.OpenAIError as e:
        return f"OpenAI API error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

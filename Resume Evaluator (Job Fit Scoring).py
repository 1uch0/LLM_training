# imports
# If these fail, please check you're running from an 'activated' environment with (llms) in the command prompt

import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI
import openai


# Initialize and constants

load_dotenv(override=True)
API_KEY = api_key

if API_KEY and API_KEY.startswith('sk-proj-') and len(API_KEY)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")

openai.api_key = API_KEY  # Set the API key directly
MODEL = 'gpt-4o-mini'
client = openai.OpenAI(api_key=API_KEY)
#openai_client = openai.OpenAI()


import openai
import json
import requests

def score_resume(job_description, resume):
    try:
        # Prepare OpenAI request
        chat_response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an HR assistant. Score resumes based on how well they match a given job description. Use a 0-100 scale and explain why."},
                {"role": "user", "content": f"Job Description: {job_description}\nCandidate Resume: {resume}\nScore this resume and justify the score."}
            ],  
            
        
        )

        # Extract the content from the response
        response_content = chat_response.choices[0].message.content

        # Return the response content
        return response_content

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
job_description = "Looking for a Psicologyst"
resume = "Experienced in AI research, proficient in Python, TensorFlow, and chatbot development."

print(score_resume(job_description, resume))


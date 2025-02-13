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
api_key = API_KEY

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")

openai.api_key = API_KEY  # Set the API key directly
MODEL = 'gpt-4o-mini'
#openai_client = openai.OpenAI()



import openai
import json
import requests
from bs4 import BeautifulSoup

# Initialize OpenAI client
client = openai.OpenAI(api_key=API_KEY)

def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract raw links
    links = [a['href'] for a in soup.find_all('a', href=True)]

    # Prepare OpenAI request
    chat_response = client.chat.completions.create(
        model=MODEL,
        messages=[
        {"role": "system", "content": "You are an expert web scraper. Extract only valid hyperlinks from a given webpage and return them in JSON."},
        {"role": "user", "content": f"Here are the extracted raw links: {links}. Filter and return only valid URLs in JSON format."}
            ],
        response_format={"type": "json_object"}   #
    )

    # Return parsed JSON response
    return json.loads(chat_response.choices[0].message.content)

# Example usage
print(extract_links("https://huggingface.co"))

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
api_key =API_KEY #put personal key here

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")

openai_client = openai.OpenAI(api_key=openai.api_key)    
    
MODEL = 'gpt-4o-mini'
#openai_client = openai.OpenAI()




# A class to represent a Webpage

# Some websites need you to use proper headers when fetching them:
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    """
    A utility class to represent a Website that we have scraped, now with links
    """

    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""
        links = [link.get('href') for link in soup.find_all('a')]
        self.links = [link for link in links if link]

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"


#######################


ed = Website("https://edwarddonner.com")
#print(ed.get_contents())
#Now we print all the links in the webpage
ed.links

######################33


link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
"""

#####
print(link_system_prompt)

############


def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt


####################


print(get_links_user_prompt(ed))



#######################


def get_links(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
      ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    return json.loads(result) #Bring as a json



#############################


get_links("https://anthropic.com")
#get_links("https://scholar.google.com/citations?user=XBEeIOcAAAAJ&hl=en")


#################################
anthropic = Website("https://anthropic.com")
anthropic.links

#############################


# Anthropic has made their site harder to scrape, so I'm using HuggingFace..

huggingface = Website("https://huggingface.co")
huggingface.links
########################

get_links("https://huggingface.co")


###########################3

def get_all_details(url):
    result = "Landing page:\n"
    result += Website(url).get_contents()
    links = get_links(url)
    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result

###########################3


print(get_all_details("https://huggingface.co"))


#############################3




system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short humorous, entertaining, jokey brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."

################################

get_brochure_user_prompt("HuggingFace", "https://huggingface.co")

#################################3


def create_brochure(company_name, url):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)} #This is going to call ChatGPT mini in order to meet the specific requirements.
          ],
    )
    result = response.choices[0].message.content
    display(Markdown(result))


###############################

create_brochure("HuggingFace", "https://huggingface.co")

#################################


#TRANSLATION PART


system_prompt_translation = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short humorous, entertaining, jokey brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information. Do all of this translated to Spanish"


###################################


def create_brochure_spanish(company_name, url):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt_translation},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)} #This is going to call ChatGPT mini in order to meet the specific requirements.
          ],
    )
    result = response.choices[0].message.content
    display(Markdown(result))


######################################



create_brochure_spanish("HuggingFace", "https://huggingface.co")


######












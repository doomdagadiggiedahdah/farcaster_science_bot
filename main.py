import os
import requests
from openai import OpenAI
import xml.etree.ElementTree as ET

client = OpenAI()
#api_key = os.getenv("OPENAI_API_KEY") ## API is by imported by default from your env variables, looks for OPENAI_API_KEY

# Construct the query URL
query = 'quantum computing'
url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=1'
response = requests.get(url)

if response.status_code == 200:
    root = ET.fromstring(response.content)
    namespace = {'arxiv': 'http://www.w3.org/2005/Atom'}
    
    for entry in root.findall('arxiv:entry', namespace):
        title = entry.find('arxiv:title', namespace).text
        abstract = entry.find('arxiv:summary', namespace).text
        
        print(f'Title: {title}\nAbstract: {abstract}')
else:
    print('Failed to fetch data from arXiv API.')

prePrompt1 = """\
Take the following text and create a viral tweet of it that makes sure to capture the intellectual richness of the text, but also encourages the reader to continue reading!
"""
text = title + abstract

def textFromAI(text):
    res = client.chat.completions.create(model = "gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": prePrompt1},
        {"role": "user", "content": text}
    ])
    story = res.choices[0].message.content
    return str(story)

print(textFromAI(text))

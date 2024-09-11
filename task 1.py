import os
import requests
import re
from bs4 import BeautifulSoup
import sys

# function to get the HTML source text of the medium article
def get_page():
    global url
    
    # Ask the user to input the Medium article URL and collect it in url
    url = input("Enter the Medium article URL: ")

    # Update the regular expression to match both 'medium.com' and 'medium.com/@username'
    if not re.match(r'https?://medium.com(/@[\w-]+)?/.+', url):
        print('Please enter a valid Medium article URL.')
        sys.exit(1)

    # Add a User-Agent header to simulate a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    # Call get method in requests object, pass url and headers, and collect it in res
    res = requests.get(url, headers=headers)

    # Ensure the request succeeded
    res.raise_for_status()

    # Parse the HTML content
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

# function to remove all the HTML tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub('\<(.*?)\>', '', text)  # Remove remaining tags
    return text

def collect_text(soup):
    text = f'url: {url}\n\n'
    para_text = soup.find_all('p')
    print(f"paragraphs text = \n {para_text}")
    for para in para_text:
        text += f"{para.text}\n\n"
    return text

# function to save the scraped text to a file
def save_file(text):
    if not os.path.exists('./scraped_articles'):
        os.mkdir('./scraped_articles')
    
    name = url.split("/")[-1]
    fname = f'scraped_articles/{name}.txt'

    # Write the text to the file
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f'File saved in directory: {fname}')


if _name_ == '_main_':
    soup = get_page()  # Get the parsed HTML of the Medium article
    text = collect_text(soup)  # Collect the text content
    save_file(text)  # Save the text content to a file

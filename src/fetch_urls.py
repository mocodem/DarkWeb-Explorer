from bs4 import BeautifulSoup
import requests
import json


def extract_onion_addresses(websites):
    onion_addresses = []
    for url in websites:
        # Get the HTML page
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        if "sitemap.xml" in url:
            internal_links = soup.find_all('loc')
            for internal_link in internal_links:
                websites.append(internal_link.text)

        # Find all links in the HTML
        links = soup.find_all('a')

        # Extract the onion addresses
        for link in links:
            href = link.get('href')
            if href and href.endswith('.onion/'):
                onion_addresses.append([href, url])
        print(f"{len(onion_addresses)} from {url}")
    return onion_addresses


def extract_ahmia(url):
    page = requests.get(url)
    links = []
    for node in json.loads(page.text).get("nodes"):
        links.append(node.get("label").replace(" ", ""))
    return links


burp0_url = "https://ahmia.fi:443/stats/static/data.json"

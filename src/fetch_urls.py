from bs4 import BeautifulSoup
import requests
import json
import httpx
import re

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


def extract_google():
    client = httpx.Client(http2=True)
    agent = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    search_string = 'site:".onion.pet"'
    try:
        response = client.get(f"https://www.google.com/search?channel=fs&client=ubuntu&q={search_string}",
                              headers=agent)
    except httpx.ConnectError:
        return []
    html = response.text
    print(html)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    # modify regex to end with .onion.pet/
    for raw_href in re.findall('href="([^"]+)"', html):
        if ".onion.pet" in raw_href[-11:]:
            links.append(raw_href)
    print(links)
    next_page = soup.find("a", {"id" : "pnnext"})
    print(next_page['href'])
    try:
        response = client.get(f"https://www.google.com/{next_page['href']}",
                              headers=agent)
    except httpx.ConnectError:
        return []
    html = response.text
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    # modify regex to end with .onion.pet/
    for raw_href in re.findall('href="([^"]+)"', html):
        if ".onion.pet" in raw_href[-11:]:
            links.append(raw_href)
    print(links)
    client.close()


extract_google()
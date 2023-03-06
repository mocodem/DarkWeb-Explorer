from fetch_urls import extract_onion_addresses, extract_ahmia
from check_urls import access_url
import oniondb
from time import sleep
import json


with open("sources/seeds.json", "r") as f:
    sources = json.loads(f.read())

urls = extract_onion_addresses(sources.get("test"))
# urls = extract_ahmia("https://ahmia.fi:443/stats/static/data.json")
print(len(urls))


for [url, source] in urls:
    url = oniondb.sanitize_url(url)
    oniondb.add_onion(url, source)
    status, captcha, captcha_type = access_url(url)
    current = oniondb.get_onion_source(url, source)
    current.status = status
    current.captcha = captcha
    current.captcha_type = captcha_type
    current.save()
    # break

print("done")

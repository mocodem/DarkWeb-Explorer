import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from PIL import Image
import time

# path to the firefox binary inside the Tor package
binary = '/home/morty/Downloads/tor-browser_en-US/Browser/firefox'
if os.path.exists(binary) is False:
    raise ValueError("The binary path to Tor firefox does not exist.")
firefox_binary = FirefoxBinary(binary)


browser = None
def get_browser(binary=None):
    global browser
    # only one instance of a browser opens, remove global for multiple instances
    if not browser:
        browser = webdriver.Firefox(firefox_binary=binary)
    return browser

if __name__ == "__main__":
    _, _, files = next(os.walk("test/images/"))
    with get_browser(binary=firefox_binary) as browser:
        print("connection check")
        browser.get("https://check.torproject.org/")
        print("connection up")
        # url = 'http://nehdddktmhvqklsnkjqcbpmb63htee2iznpcbs5tgzctipxykpj6yrid.onion/nojs/captcha' #text 1
        # url = 'http://4usoivrpy52lmc4mgn2h34cmfiltslesthr56yttv2pxudd3dapqciyd.onion/blockBypass.js' # text 2
        # url = 'http://eux4gt4qcaiesps5w5rppxcenoe5shapwycums5yuiikmc4mpc74gpyd.onion/register.php' # text 3
        # url = 'http://cebulka7uxchnbpvmqapg5pfos4ngaxglsktzvha7a5rigndghvadeyd.onion/' # text 4
        # url = 'http://dnmxjaitaiafwmss2lx7tbs5bv66l7vjdmb5mtb3yqpxqhk3it5zivad.onion/register.php' # text 5
        # url = 'http://loginzlib2vrak5zzpcocc3ouizykn6k5qecgj2tzlnab5wcbqhembyd.onion/registration.php' # text 6
        # url = 'http://3gfrhqleclu65nh5niz76d74e7rvangnb4qwzeu73qsanhinbqbmbiyd.onion/register' # text 7
        # url = 'http://darkchatzmuji2lievi7ekljno3p6vdb355p3qvoxcpm7nfhs7k6xcid.onion/webclient.html#converse/register' # numbers 1
        # url = 'http://6esdfufqqmovn6ihv3r5lzgsdgrf6auc43itgwqa6w3dy4bymki3clid.onion/chat.php' # numbers 2
        # url = 'http://6c5qaeiibh6ggmobsrv6vuilgb5uzjejpt2n3inoz2kv2sgzocymdvyd.onion/signin' # numbers 3
        # url = 'http://pt2mftbxeczbzufi2v7b3ekmsun4khq6hi7bdjo7w23fsx3easvr73ad.onion/' # numbers 4
        #  1 0.426357 0.646425 0.145349 0.039836
        # Others
        # url = 'http://dkforestseeaaq2dqz2uflmlsybvnq2irzn4ygyvu53oazyorednviid.onion/signup' # numbers and wires
        # 2 0.499516 0.517227 0.237403 0.128122
        url = "http://xv3dbyx4iv35g7z2uoz2yznroy56oe32t7eppw2l2xvuel7km2xemrad.onion/" # clock
        # many others from marketplaces
        captcha_type = "test"
        print("connecting to host")
        browser.get(url)
        input()
        print("screenshooting")
        browser.save_screenshot(f'test/{captcha_type}_{len(files)}.png')

        input()
        browser.refresh()

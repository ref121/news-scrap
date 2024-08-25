import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import scrap_kit as sk
from pprint import pprint
from article import Article
from web_image import Image
import json
import re




        

# # will install local 
chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
# Navigate to the page
driver.get(sk.GEEK_MAIN_PAGE)

# Wait for the page to load and for the specific elements to be present
wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
articles = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, sk.GEEK_HEADER_ARTICLES_LIST))
)
sub_headers = driver.find_elements(By.XPATH, sk.GEEK_SUB_HEADERS_ARTICLES)
sub_headers = [sub.text for sub in sub_headers]
images_url = driver.find_elements(By.XPATH, sk.IMAGE_GEEK_OBJECTS_LIST)
headers = []
authors = []
for article in articles:
    headers.append(article.get_attribute('data-title'))
    authors.append(article.get_attribute('data-author'))
images_url = [img.get_attribute('src') for img in images_url]

articles = [Article(headers[i], sub_headers[i], Image(images_url[i]).download_image(), authors[i]).to_dict() for i in range(len(headers))]
articles = json.dumps(articles, indent=4)
print(articles) 



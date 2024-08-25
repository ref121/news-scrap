import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import scrap_kit as sk
import time
from article import Article
from web_image import Image
from pprint import pprint
import json

# scrap the first six articles return nested list that each cell contains: header, sub_header, author of those articles
def get_first_six_article_elements() -> list:
    elements = driver.find_elements(By.XPATH, sk.ACTUAL_6_ELEMENT_12)
    element_order_list = []
    for element in elements:
        temp_list = []
        for line in element.text[::-1].splitlines(): # the string came reverse its needed to reverse
            temp_list.append(line)
        element_order_list.append(temp_list)
    return element_order_list


# return a list that containes [header, sub header] of all articles
def clear_author_from_article(articles)-> list:
    head_and_sub = []
    for article in articles:
        temp_list = [] # will take a header and sub of current article
        for i in range(1,len(article)):
            temp_list.append(sk.fix_hebrew_english_mix(article[i]))
        head_and_sub.append(temp_list) # add the header + sub header as a list inside the list
    return head_and_sub

# return a list that contains only the headers
def get_headers(articles)-> list:
    return [articles[i][0] for i in range(len(articles))]

# get sub headers ffrom articles
def get_sub_headers(articles:list)-> list:
    return [articles[i][1] for i in range(len(articles))]

# return clean list that contains the authors onlly
def get_authors_from_article(articles:list)-> list:
    authors = [articles[i][0] for i in range(len(articles))]
    authors_names = [sk.fix_hebrew_english_mix(authors[i][authors[i].index('|')+1::]) for i in range(len(authors))]
    return [clean_name.replace(',','') for clean_name in authors_names]
    

# get the image urls for downloading -> return a list that contains the images urls according the articles order
def get_first_six_images_url()-> list:
    elements = driver.find_elements(By.XPATH,sk.ACTUAL_6_PICTURES_12)
    return [element.get_attribute('src') for element in elements]

# will install the current virsion of chrome 
chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get(sk.ACTUAL_PAGE_12)

time.sleep(3)

elements = get_first_six_article_elements() # contains the all articles with the all atributes

authors = get_authors_from_article(elements) # getting the authors

elements = clear_author_from_article(elements) # elements now with header and subheaders anly

image_urls = get_first_six_images_url() # getting the urls for downloading


headers = get_headers(articles=elements) 

sub_headers = get_sub_headers(articles=elements)

''' articles will contain a list of dictionary of article class
 pay attension that download image method that implement here return the object it self for the constructor,
 because after the to_dict() method the object is no longer an object for the compiler, and so the download_image()
 method cannot execute after it, thats why the download_image() method return the object its self
 '''
articles = [Article(headers[i],sub_headers[i], Image(image_urls[i]).download_image(), authors[i]).to_dict() for i in range(6)]




"""
    save the articles as a json file and print it to pass the json via subprocess that web.py execute
"""
articles = json.dumps(articles, indent=4)
print(articles) 
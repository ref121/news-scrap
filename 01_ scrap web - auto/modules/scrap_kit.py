import re


# N12
ACTUAL_PAGE_12 = 'https://www.mako.co.il/news-dailynews?partner=NewsNavBar'

ACTUAL_6_ELEMENT_12 = '//ul[@class="grid-ordering mainItem6"]/li'
ACTUAL_6_PICTURES_12 = '//ul[@class="grid-ordering mainItem6"]//li//img'


# Geek Time
GEEK_MAIN_PAGE = 'https://www.geektime.co.il/'
GEEK_HEADER_ARTICLES_LIST = '//*[@id="news_posts"]/article[@data-title]'
GEEK_SUB_HEADERS_ARTICLES = '//*[@id="news_posts"]/article/div/div[2]/a/div'
IMAGE_GEEK_OBJECTS_LIST = '/html/body/main/section[2]/div/div[3]/div[3]/div[2]/article/div/div[1]/a/img'

# Encoded the hebrew sentence also if english letters included
def fix_hebrew_english_mix(text):
    # Split the text into words
    words = re.findall(r'\S+', text)
    
    # Reverse the order of words
    words.reverse()
    
    # Function to check if a word is primarily Hebrew
    def is_hebrew(word):
        return any('\u0590' <= char <= '\u05FF' for char in word)
    
    # Process each word
    for i, word in enumerate(words):
        if is_hebrew(word):
            # Reverse Hebrew words back to correct order
            words[i] = word[::-1]
        # English words and punctuation remain as is
    
    # Join the words back into a sentence
    return ' '.join(words)
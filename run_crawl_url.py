from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from time import sleep
import os
import pymongo

load_dotenv()
use_chrome = os.environ.get('USE_CHROME')
driver_path = os.environ.get('CHROMEDRIVER_PATH')
user_chrome_dir = os.environ.get('USER_CHROME_DIR')
raw_file = os.environ.get('RAW_URL_FILE')
non_crawl_file = os.environ.get('NON_CRAWL_FILE')
crawled_file = os.environ.get('CRAWLED_FILE')
error_file = os.environ.get('ERROR_FILE')
max_crawl_time = int(os.environ.get('MAX_CRAWL_TIME'))
timeout = float(os.environ.get('TIMEOUT'))
db_uri = os.environ.get('MONGODB_DATABASE_URI')
db_name = os.environ.get('MONGODB_DATABASE_NAME')
timeout = float(os.environ.get('TIMEOUT'))

options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")
driver = uc.Chrome(options=options)

crawl_category_url = [
    {
        "category": "development",
        "sub": ['web-development', 'data-science', 'mobile-apps', 'programming-languages', 'game-development', 'databases', 'software-testing', 'software-engineering', 'development-tools', 'no-code-development']
    },
    {
    "category": "business",
    "sub": ['entrepreneurship','communications','management','sales','strategy','operations','project-management','business-law','analytics-and-intelligence','human-resources','industry','e-commerce','media','real-estate','other-business']

    },
    {
    "category": "finance-and-accounting",
    "sub": ['accounting-bookkeeping','compliance','cryptocurrency-and-blockchain','economics','finance-management','finance-certification-and-exam-prep','financial-modeling-and-analysis','investing-and-trading','money-management-tools','taxes','other-finance-and-accounting']
    },
    {
    "category": "it-and-software",
    "sub": ['it-certification','network-and-security','hardware','operating-systems','other-it-and-software']
    },
    {
    "category": "office-productivity",
    "sub": ['microsoft','apple','sap','oracle','other-productivity']
    },
    {
    "category": "personal-development",
    "sub": ['personal-transformation','productivity','leadership','career-development','parenting-and-relationships','happiness','esoteric-practices','religion-and-spirituality','personal-brand-building','creativity','influence','self-esteem-and-confidence','stress-management','memory','motivation','other-personal-development']
    },
    {
    "category": "design",
    "sub": ['web-design','graphic-design-and-illustration','design-tools','user-experience','game-design','3d-and-animation','fashion','architectural-design','interior-design','other-design']
    },
    {
    "category": "marketing",
    "sub": ['digital-marketing','search-engine-optimization','social-media-marketing','branding','marketing-fundamentals','analytics-and-automation','public-relations','advertising','video-and-mobile-marketing','content-marketing','growth-hacking','affiliate-marketing','product-marketing','other-marketing']
    },
    {
    "category": "lifestyle",
    "sub": ['arts-and-crafts','beauty-and-makeup','esoteric-practices','food-and-beverage','gaming','home-improvement','pet-care-and-training','travel','other-lifestyle']
    },
    {
    "category": "photography-and-video",
    "sub": ['digital-photography','photography-fundamentals','portraits','photography-tools','commercial-photography','video-design','other-photography-and-video']
    },
    {
    "category": "health-and-fitness",
    "sub": ['fitness','general-health','sports','nutrition','yoga','mental-health','self-defense','safety-and-first-aid','dance','meditation','other-health-and-fitness']
    },
    {
    "category": "music",
    "sub": ['instruments','production','music-fundamentals','vocal','music-techniques','music-software','other-music']
    },
    {
    "category": "teaching-and-academics",
    "sub": ['engineering','humanities','math','science','online-education','social-science','language','teacher-training','test-prep','other-teaching-academics']
    },
]

with driver:
    from_page = 0
    to_page = 625
    urls = []
    page_count = 0
    for category in crawl_category_url:
        for sub_category in category['sub']:
            for page_num in range(from_page, to_page):
                raw_urls = []
                url = "https://www.udemy.com/courses/" + str(category['category']) + "/" + str(sub_category) + "/?p=" + str(page_num+1)
                driver.get(url)
                sleep(timeout * 1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(timeout * 0.2)
                target = driver.find_elements(By.CSS_SELECTOR, '.course-directory--container--2H7uM .course-card-title-module--title--2C6ac a')
                for item in target:
                    href = item.get_attribute('href')
                    raw_urls.append(href)
                print("\n\n\n", raw_urls)
                if len(raw_urls) > 0:
                    for item in raw_urls:
                        urls.append(item)
                    page_count += 1
                else:
                    break
                if int(page_count) % 25 == 0:
                    data = []
                    for url in urls:
                        url = str(url.strip())
                        data.append({"url": url, "status": False})
                    mongo_client = pymongo.MongoClient(db_uri)
                    mongo_db = mongo_client[db_name]
                    collection = mongo_db["url"]
                    collection.insert_many(data)
                    urls = []
            
        for url in urls:
            url = str(url.strip())
            data.append({"url": url, "status": False})

    mongo_client = pymongo.MongoClient(db_uri)
    mongo_db = mongo_client[db_name]
    collection = mongo_db["url"]
    collection.insert_many(data)

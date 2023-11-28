from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from time import sleep
import selenium_funcs
import database_funcs
import os
import pymongo

if __name__ == "__main__":
    load_dotenv()
    use_chrome = os.environ.get('USE_CHROME')
    driver_path = os.environ.get('CHROMEDRIVER_PATH')
    user_chrome_dir = os.environ.get('USER_CHROME_DIR')
    raw_file = os.environ.get('RAW_URL_FILE')
    non_crawl_file = os.environ.get('NON_CRAWL_FILE')
    crawled_file = os.environ.get('CRAWLED_FILE')
    error_file = os.environ.get('ERROR_FILE')
    max_page = int(os.environ.get('MAX_PAGE'))
    max_crawl_time = int(os.environ.get('MAX_CRAWL_TIME'))
    number_of_crawl_machine = int(os.environ.get('NUMBER_OF_CRAWL_MACHINE'))
    timeout = float(os.environ.get('TIMEOUT'))
    db_uri = os.environ.get('MONGODB_DATABASE_URI')
    db_name = os.environ.get('MONGODB_DATABASE_NAME')
    mongo_client = pymongo.MongoClient(db_uri)
    mongo_db = mongo_client[db_name]

    
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    driver = uc.Chrome(options=options)
    with driver:
        database_funcs.get_course_url_list(mongo_db, non_crawl_file, crawled_file)
        if os.path.exists(error_file)!=True:
            with open(error_file, "w") as file:
                file.write("")
        sucess_course_arr, sucess_url_id_arr, error_url_arr = selenium_funcs.crawl_course_detail(driver, number_of_crawl_machine, non_crawl_file, crawled_file, error_file, timeout, max_crawl_time, mongo_db)
        database_funcs.add_crawled_course_detail_to_db(mongo_db, sucess_course_arr)
        database_funcs.change_success_url_status(mongo_db, sucess_url_id_arr)
        with open(error_file, 'w') as file:
            for url in error_url_arr:
                file.write(str(url) + '\n')
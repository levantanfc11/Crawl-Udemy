from time import sleep
from selenium.webdriver.common.by import By
import database_funcs

def get_raw_url(driver, file_path, max_page, timeout):
    with open(file_path, 'w') as file:
        categories = ["it-certification", "network-and-security"]
        # categories = ["it-certification"]
        for page_num in range(max_page):
            for category in categories:
                url = "https://www.udemy.com/courses/it-and-software/" + category + "/?p=" + str(page_num+1)
                driver.get(url)
                sleep(timeout * 1.5)
                target = driver.find_elements(By.CSS_SELECTOR, '.course-card-title-module--title--2C6ac a')
                for item in target:
                    href = item.get_attribute('href')
                    file.write(str(href) + '\n')

def crawl_course_detail(driver, number_of_crawl_machine, processing_file, done_file, error_file, timeout, max_crawl_time, mongo_db):
    error_time=0
    crawl_time=0
    skip_url=55*int(number_of_crawl_machine-1)
    max_err_time=30000
    raw_url_data = []
    done_url_arr = []
    error_url_arr = []
    sucess_url_id_arr= []
    sucess_course_arr= []
    with open(processing_file, 'r+') as file:
        raw_url_data = file.readlines()
        raw_url_data = raw_url_data[skip_url:]
    with open(done_file, 'r+') as file:
        done_url_arr = file.readlines()
        if len(done_url_arr) == 0:
            done_url_arr.append("")
    with open(error_file, 'r+') as file:
        error_url_arr = file.readlines()
    for course in raw_url_data:
        if error_time<max_err_time and crawl_time<max_crawl_time:
            course = course.split(",")
            course_id = course[0]
            url = course[1]
            if url in done_url_arr[0] or course_id in error_url_arr or course_id in sucess_url_id_arr:
                continue
            driver.get(url)
            sleep(timeout * 1)

            try:
                show_more_btn = driver.find_element(By.CSS_SELECTOR, '.course-landing-page__main-content .what-you-will-learn--what-will-you-learn--1nBIT span.show-more-module--show-more--2bohq')
                show_more_btn.click()
            except:
                pass
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            sleep(timeout/2)
            driver.execute_script("window.scrollTo(document.body.scrollHeight/2, document.body.scrollHeight);")
            sleep(timeout/2)

            try:
                title_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div[1]/div/div/div[3]/div/h1').text
                try:  
                    category_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div[1]/div/div/div[1]/div/a[2]').text
                except:
                    category_element = ""
                try:
                    skill_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div[1]/div/div/div[1]/div/a[3]').text
                except:
                    skill_element = ""
                try:
                    describe_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/main/div[1]/div/div/div[3]/div/div[1]').text
                except:
                    describe_element = ""
                try:
                    average_rating_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/main/div[1]/div/div/div[3]/div/div[2]/div/a/span[1]/span[2]").text
                except:
                    average_rating_element = "none"
                try:
                    best_seller_element = driver.find_element(By.XPATH, ".clp-lead__badge-ratings-enrollment .course-badges-module--bestseller--2k308").text
                    best_seller_element = True
                except:
                    best_seller_element = False
                try:
                    review_count_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/main/div[1]/div/div/div[3]/div/div[2]/div/a/span[2]").text
                    review_count_element = review_count_element.replace("ratings", "").replace(",", "").replace(".", "").replace("(", "").replace(")", "").strip()
                except:
                    review_count_element = ""
                try:
                    students_enrolled_element = driver.find_element(By.CSS_SELECTOR, '.clp-lead__badge-ratings-enrollment .enrollment').text
                    students_enrolled_element = students_enrolled_element.replace("students","").replace(",", "").replace(".", "").strip()
                except:
                    students_enrolled_element = ""
                try:
                    language_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/main/div[1]/div/div/div[3]/div/div[4]/div[2]").text
                except:
                    language_element = ""
                try:
                    price_element = driver.find_element(By.CSS_SELECTOR, ".sidebar-container--content--2KZyB .purchase-section-container--purchase-section-container--1wStb .price-text--container--103D9 .price-text--price-part--2npPm.ud-heading-xxl span span").text.strip()
                except:
                    try:
                        price_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/main/div[3]/div[1]/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/span[2]/span").text.strip()
                    except:
                        price_element = ""
                try:
                    study_time_element = driver.find_element(By.CSS_SELECTOR, ".curriculum--curriculum-sub-header--m_N_0 div span.curriculum--content-length--5Nict").text
                except:
                    study_time_element = ""
                try:
                    gain_exp_elements = driver.find_elements(By.CSS_SELECTOR, ".what-you-will-learn--content-spacing--3n5NU li span")
                    gain_exp_list = []
                    for gain_exp in gain_exp_elements:
                        gain_exp_list.append(gain_exp.text)
                except:
                    gain_exp_list = []
                try:
                    xpath = '//*[@id="main-content-anchor"]//div[@class="instructor--instructor--2sjZy"]'
                    organi_list_element = driver.find_elements(By.XPATH, xpath)
                    organi_element = []
                    for index in range(len(organi_list_element)):
                        index+=1
                        tc_name = driver.find_element(By.XPATH, f'{xpath}[{index}]//div[1]//div[1]//a').text
                        tc_job = driver.find_element(By.XPATH, f'{xpath}[{index}]//div[1]//div[2]').text
                        tc_image = driver.find_element(By.XPATH, f'{xpath}[{index}]//div[2]//a//img').get_attribute("src")
                        tc_student_count = driver.find_element(By.XPATH, f'{xpath}[{index}]//div[2]//ul//li[3]//div//div').text
                        tc_course_count = driver.find_element(By.XPATH, f'{xpath}[{index}]//div[2]//ul//li[4]//div//div').text
                        organi_element.append({
                            "teacher_name": tc_name,
                            "teacher_job": tc_job,
                            "teacher_image": tc_image,
                            "teacher_count_student": tc_student_count.replace("Students","").strip(),
                            "teacher_count_course": tc_course_count.replace("Courses","").strip(),
                        })
                except:
                    organi_element = []

                title = title_element
                organi = organi_element
                category = category_element
                best_seller = best_seller_element
                skill = skill_element
                describe = describe_element
                students_enrolled = students_enrolled_element
                study_time = study_time_element
                language = language_element
                average_rating = average_rating_element
                review_count = review_count_element

                entry = {
                    "title": title,
                    "best_seller": best_seller,
                    "price": price_element,
                    "organi": organi,
                    "skill": skill,
                    "category": category,
                    "gain_exp_list": gain_exp_list,
                    "describe": describe,
                    "students_enrolled": students_enrolled,
                    "study_time": study_time,
                    "language": language,
                    "average_rating": average_rating,
                    "review_count": review_count,
                    "url_id": course_id
                }
                sucess_course_arr.append(entry)
                sucess_url_id_arr.append(course_id)
                print("\n\n ========> Crawl lần thứ " + str(crawl_time+1) + ": " + str(entry))
            except Exception as e:
                print("\n\n===> Lỗi " + str(e) + "\n")
                error_url_arr.append(course_id)
                error_time+=1
            finally:
                crawl_time+=1
                print("===> Còn lại " + str(max_crawl_time-crawl_time))
                if len(sucess_url_id_arr)>=50:
                    database_funcs.add_crawled_course_detail_to_db(mongo_db, sucess_course_arr)
                    database_funcs.change_success_url_status(mongo_db, sucess_url_id_arr)
                    sucess_course_arr = []
                    sucess_url_id_arr = []
                    database_funcs.get_course_url_list(mongo_db, processing_file, done_file)
                    with open(processing_file, 'r+') as file:
                        raw_url_data = file.readlines()
                        raw_url_data = raw_url_data[skip_url:]
                    with open(done_file, 'r+') as file:
                        done_url_arr = file.readlines()
                        if len(done_url_arr) == 0:
                            done_url_arr.append("")
                    sleep(timeout * 0.2)
        else:
            break
    return sucess_course_arr, sucess_url_id_arr, error_url_arr
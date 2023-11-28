from time import sleep
from bson import ObjectId

def url_collection():
    return "url"

def course_collection():
    return "course"

def add_url_to_database(mongo_db, file_path):
    collection = mongo_db[url_collection()]
    data = []
    with open(file_path, "r") as file:
        urls = file.readlines()
    for url in urls:
        url = str(url.strip())
        data.append({"url": url, "status": False})
    collection.insert_many(data)

def get_course_url_list(mongo_db, non_crawl_file, crawled_file):
    collection = mongo_db[url_collection()]
    non_crawl_urls = collection.find({"status": False})
    crawled_urls = collection.find({"status": True})
    with open(non_crawl_file, 'w') as file:
        for url in non_crawl_urls:
            file.write(str(url["_id"]) + "," + str(url["url"]) + '\n')
    with open(crawled_file, 'w') as file:
        for url in crawled_urls:
            file.write(str(url["url"]))
    
def add_crawled_course_detail_to_db(mongo_db, sucess_course_arr):
    collection = mongo_db[course_collection()]
    collection.insert_many(sucess_course_arr)
    print("\n\t\t===> Đã cập nhật dữ liệu vào database <===")

def change_success_url_status(mongo_db, sucess_url_id_arr):
    object_ids = [ObjectId(id) for id in sucess_url_id_arr]
    collection = mongo_db[url_collection()]
    collection.update_many({"_id": {"$in": object_ids}}, {"$set": {"status": True}})
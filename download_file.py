import requests
import mysql.connector
import time
import os
from urllib.parse import urlparse
from slugify import slugify
import schedule
import time
from datetime import datetime


def main():
    folder_path = "F:\ebook2"
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ebook_crawl"
    )

    cursor = conn.cursor()
    select = "SELECT id, name_file, file_type, download FROM ebook WHERE is_file = 0 LIMIT 1"
    cursor.execute(select)
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        name_file = row[1]
        file_type = row[2].lower()
        url = row[3]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.06',
        }
        proxies = {
            "https": '103.231.248.98:3128',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            name_file_slug = slugify(name_file)
            file_name = f"{id}-{name_file_slug}.{file_type}"
            destination = os.path.join(folder_path, file_name)
            with open(destination, 'wb') as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)

            update = f"UPDATE `ebook` SET `is_file` = 1, `file_path` = %s  WHERE `id` = {id}"
            cursor.execute(update, (file_name,))
            conn.commit()

            # Lấy thời gian hiện tại
            current_time = datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")
            print(f"DOWNLOAD OK - {id} - {formatted_time}")
        else:
            # update = f"UPDATE `ebook` SET `is_file` = -1 WHERE `id` = {id}"
            # cursor.execute(update)
            # conn.commit()
            # print(f"FALSE - {id}")
            current_time = datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")
            print(f"No - {response.status_code} - {formatted_time}")


schedule.every(1).seconds.do(main)
schedule.run_all()
while True:
    schedule.run_pending()
    time.sleep(1)

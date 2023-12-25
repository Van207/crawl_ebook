import requests
import mysql.connector
from datetime import datetime
from bs4 import BeautifulSoup
import schedule
import time
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ebook_crawl"
)


def main():
    cursor = conn.cursor()
    select = "SELECT id, url FROM url WHERE status = 0 ORDER BY id ASC LIMIT 1"
    cursor.execute(select)
    results = cursor.fetchall()
    if len(results) > 0:
        for row in results:
            url_id = row[0]
            url = row[1]
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                if soup.select_one('h1.post-title'):
                    title = soup.select_one('h1.post-title').get_text().strip()
                    # print(title)
                else:
                    update = f"UPDATE `url` SET `status` = -1 WHERE `id` = {url_id}"
                    cursor.execute(update)
                    conn.commit()
                    print(f"FALSE - {url_id}")

                if soup.select_one('a.btn-slide2'):
                    dowload_link = soup.select_one('a.btn-slide2').get('href')
                    # print(dowload_link)
                else:
                    update = f"UPDATE `url` SET `status` = -1 WHERE `id` = {url_id}"
                    cursor.execute(update)
                    conn.commit()
                    print(f"FALSE - {url_id}")

                if soup.select('.post-body.entry-content ul li'):
                    name = ""
                    file_type = ""
                    capacity = ""
                    page = ""
                    li_elements = soup.select('.post-body.entry-content ul li')
                    for li_element in li_elements:
                        li_text = li_element.get_text().strip()

                        # Lấy tên file
                        if li_text.lower().startswith('tên'):
                            name = li_text.split(':')[1].strip()
                            # print(name)

                        # Lấy loại file
                        if li_text.lower().startswith('loại'):
                            file_type = li_text.split(':')[1].strip()
                            # print(file_type)
                        # else:
                        #     file_type = ""

                        # Lấy dung lượng
                        if li_text.lower().startswith('dung'):
                            capacity = li_text.split(':')[1].strip()
                            # print(capacity)

                        # Lấy số trang
                        if li_text.lower().startswith('số'):
                            page = li_text.split(':')[1].strip()
                            # print(page)

                    insert_ebook = f"INSERT INTO `ebook`(`url_id`, `title`, `name_file`, `file_type`, `capacity`, `page`, `download_link`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(
                        insert_ebook, (url_id, title, name, file_type, capacity, page, dowload_link))

                    update = f"UPDATE `url` SET `status` = 1 WHERE `id` = {url_id}"
                    cursor.execute(update)
                    conn.commit()
                    print(f"OK - {url_id}")
            else:
                print(f'Lỗi: {response.status_code}')
                update = f"UPDATE `url` SET `status` = -1 WHERE `id` = {url_id}"
                cursor.execute(update)
                conn.commit()
                print(f"FALSE - {url_id}")


schedule.every(1).seconds.do(main)
schedule.run_all()
while True:
    schedule.run_pending()
    time.sleep(0.2)

import requests
import mysql.connector
import time

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ebook_crawl"
)
select = "SELECT id, download_link FROM ebook WHERE download = ''"
cursor = conn.cursor()
cursor.execute(select)
results = cursor.fetchall()
for row in results:
    id = row[0]
    download_link = row[1]
    urlid = download_link.split('id=')[1]
    download = "https://drive.google.com/uc?export=download&confirm=f&id=" + urlid
    update = f"UPDATE `ebook` SET download = %s WHERE id = %s"
    print(id)
    cursor.execute(update, (download, id))
    conn.commit()
    # print(download)

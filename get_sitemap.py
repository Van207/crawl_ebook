import requests
import xml.etree.ElementTree as ET
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ebook_crawl"
)
cursor = conn.cursor()
for i in range(1, 9):

    url = f"https://thuvienpro.blogspot.com/sitemap.xml?page={i}"
    response = requests.get(url)
    if response.status_code == 200:
        insert = f"INSERT INTO `url`(`url`, `status`) VALUES (%s, %s)"
        root = ET.fromstring(response.content)
        for url_element in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url_element.find(
                '{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
            cursor.execute(insert, (loc, '0'))
            conn.commit()
            print(f"{i} - {loc}")

    else:
        print(f'Lỗi: {response.status_code}')

import requests
from bs4 import BeautifulSoup
import sqlite3
import sqlite3 as sql

#Site bağlantı adresleri
idefix_url = "https://www.idefix.com/CokSatanlar/Kitap"
amazon_url = "https://www.amazon.com.tr/gp/bestsellers/books/?ie=UTF8&ref_=sv_books_1"
dr_url = "https://www.dr.com.tr/CokSatanlar/Kitap"
kidega_url = "https://kidega.com/cok-satan-kitaplar"

idefix_html = requests.get(idefix_url).content
amazon_html = requests.get(amazon_url).content
dr_html = requests.get(dr_url).content
kidega_html = requests.get(kidega_url).content

soup = BeautifulSoup(idefix_html, "html.parser")
soup2 = BeautifulSoup(amazon_html, "html.parser")
soup3 = BeautifulSoup(dr_html, "html.parser")
soup4 = BeautifulSoup(kidega_html, "html.parser")

#Kitapların verilerin çekilecek olan adresleri
idefix_list = soup.find_all("div",{"class": "product-info"}, limit = 10)
amazon_list = soup2.find_all("div", {"class": "a-section a-spacing-none aok-relative"}, limit= 10)
dr_list = soup3.find_all("div", {"class": "content"}, limit = 10)
kidega_list = soup4.find_all("div", {"class": "newItem"}, limit = 10)

#print("*****IDEFIX*****")

#for döngüsü ile tek tek ekrana basma ve SQLITE3'e yükleme
for idefix_div in idefix_list:
    writer    = idefix_div.find("div", {"class": "box-line-2 pName"}).find("a").text
    booktitle = idefix_div.find("div", {"class": "box-title"}).find("a").text
    oldprace  = idefix_div.find("span", {"class": "old-price"}).text
    newprace  = idefix_div.find("span", {"class": "price price"}).text
    #print(f"Yazar: {writer.ljust(20)} Kitap: {booktitle.ljust(60)} Ücret: {oldprace} İndirimli Ücreti: {newprace}")

    vt = sql.connect('Cok_Okunan_Kitaplar.db')
    im = vt.cursor()
    print("Bağlantı kuruldu...")
    im.execute("""CREATE TABLE IF NOT EXISTS 'IDEFIX'
        ('Yazar', 'Kitap', 'Ucret','Indirimli_Ucret')""")
    im.execute("INSERT INTO IDEFIX (Yazar, Kitap, Ucret, Indirimli_Ucret) VALUES (?, ?, ?, ? )", (writer,booktitle,oldprace,newprace,))
    print("Database eklendi...")
    vt.commit()

#print("*****AMAZON*****")

for amazon_div in amazon_list:
    writer_amazon = amazon_div.find("div", {"class": "a-row a-size-small"}).find("span").text
    booktitle_amazon = amazon_div.find("a", {"class": "a-link-normal"}).text
    oldprace_amazon = amazon_div.find("span", {"class": "p13n-sc-price"}).text
    #print(f"Yazar: {writer_amazon.ljust(20)[0:15]} Kitap: {booktitle_amazon.strip().ljust(60)[0:15]} Ücret: {oldprace_amazon}")

    vt = sql.connect('Cok_Okunan_Kitaplar.db')
    im = vt.cursor()
    im.execute("""CREATE TABLE IF NOT EXISTS 'AMAZON'
        ('Yazar', 'Kitap', 'Ucret')""")
    im.execute("INSERT INTO AMAZON (Yazar, Kitap, Ucret ) VALUES (?, ?, ?)", (writer_amazon,booktitle_amazon.strip(),oldprace_amazon,))
    print("Database eklendi...")
    vt.commit()

#print("*****DR*****")

for dr_div in dr_list:
    writer_dr = dr_div.find("a", {"class": "who"}).text
    booktitle_dr = dr_div.find("a", {"class": "item-name"}).find("h3").text
    oldprace_dr = dr_div.find("span", {"class": "old-price"}).text
    newprace_dr = dr_div.find("span", {"class": "price"}).text
    #print(f"Yazar: {writer_dr.ljust(20)} Kitap: {booktitle_dr.ljust(60)} Ücret: {oldprace_dr} İndirimli Ücreti: {newprace_dr} ")

    vt = sql.connect('Cok_Okunan_Kitaplar.db')
    im = vt.cursor()
    im.execute("""CREATE TABLE IF NOT EXISTS 'DR'
        ('Yazar', 'Kitap', 'Ucret','Indirimli_Ucret')""")
    im.execute("INSERT INTO DR (Yazar, Kitap, Ucret,Indirimli_Ucret) VALUES (?, ?, ?, ? )", (writer_dr,booktitle_dr,newprace_dr,newprace_dr,))
    print("Database eklendi...")
    vt.commit()

#print("*****KİDEGA*****")

for kidega_div in kidega_list:   
    writer_kidega = kidega_div.find("div", {"class": "authorArea"}).find("a").text
    booktitle_kidega = kidega_div.find("a", {"class": "book-name"}).text
    oldprace_kidega = kidega_div.find("div", {"class": "itemFooter"}).find("u").text
    newprace_kidega = kidega_div.find("div", {"class": "itemFooter"}).find("b").text
    #print(f"Yazar: {writer_kidega.ljust(20)[0:15]} Kitap: {booktitle_kidega.ljust(60)} Ücret: {oldprace_kidega} İndirimli Ücret: {newprace_kidega} ")
    
    vt = sql.connect('Cok_Okunan_Kitaplar.db')
    im = vt.cursor()
    im.execute("""CREATE TABLE IF NOT EXISTS 'KIDEGA'
        ('Yazar', 'Kitap', 'Ucret','Indirimli_Ucret')""")
    im.execute("INSERT INTO KIDEGA (Yazar, Kitap,Ucret,Indirimli_Ucret) VALUES (?, ?, ?, ? )", (writer_kidega,booktitle_kidega,oldprace_kidega,newprace_kidega,))
    print("Database eklendi...")
    vt.commit()

vt.close()
print("Bağlantı kapatıldı...")

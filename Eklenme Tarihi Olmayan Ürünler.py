import requests
from bs4 import BeautifulSoup
url = "https://docs.google.com/spreadsheets/d/1AP9EFAOthh5gsHjBCDHoUMhpef4MSxYg6wBN0ndTcnA/edit#gid=0"
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")
first_cell = soup.find("td", {"class": "s2"}).text.strip()
if first_cell != "Aktif":
    exit()
first_cell = soup.find("td", {"class": "s1"}).text.strip()
print(first_cell)

import pandas as pd
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from io import BytesIO
import os
import numpy as np
import shutil
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from selenium.common.exceptions import TimeoutException, WebDriverException
import xml.etree.ElementTree as ET
import warnings
from colorama import init, Fore, Style
import openpyxl
from openpyxl import load_workbook
import threading
from selenium.common.exceptions import TimeoutException, NoSuchElementException
warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None


print("Oturum Açma Başarılı Oldu")
print(" /﹋\ ")
print("(҂`_´)")
print(Fore.RED + "<,︻╦╤─ ҉ - -")
print("/﹋\\")
print("Mustafa ARI")
print(" ")



#region Ürün Listesi İndirme

def download_and_merge_excel(url1, url2, url3):
    response1 = requests.get(url1)
    with open('excel1.xlsx', 'wb') as f1:
        f1.write(response1.content)
    response2 = requests.get(url2)
    with open('excel2.xlsx', 'wb') as f2:
        f2.write(response2.content)
    response3 = requests.get(url3)
    with open('excel3.xlsx', 'wb') as f3:
        f3.write(response3.content)
    
    df1 = pd.read_excel('excel1.xlsx')
    df2 = pd.read_excel('excel2.xlsx')
    df3 = pd.read_excel('excel3.xlsx')
    
    merged_df = pd.concat([df1, df2, df3], ignore_index=True)
    merged_df.to_excel('UrunListesi.xlsx', index=False)
    
    os.remove('excel1.xlsx')
    os.remove('excel2.xlsx')
    os.remove('excel3.xlsx')

if __name__ == "__main__":
    url1 = "https://task.haydigiy.com/FaprikaXls/GERVEF/1/"
    url2 = "https://task.haydigiy.com/FaprikaXls/GERVEF/2/"
    url3 = "https://task.haydigiy.com/FaprikaXls/GERVEF/3/"
    download_and_merge_excel(url1, url2, url3)

print(Fore.YELLOW + "Ürün Listesi İndirildi")

#endregion

#region Belli Sütunlar Hariç Diğerlerini Silme

# Exceli Okuma
df_merged = pd.read_excel('UrunListesi.xlsx')

# Sütunları Belirle
columns_to_keep = ["UrunAdi", "AramaTerimleri"]

# Sil
df_merged = df_merged[columns_to_keep]

# Exceli Kaydet
df_merged.to_excel('UrunListesi.xlsx', index=False)

print(Fore.YELLOW + "Calışma Alanı Oluşturuldu ve Gereksiz Sütunlar Silindi")

#endregion

#region Arama Terimlerindeki Tarihleri Tespit Edip Çıkarma


# Exceli Oku
df_calisma_alani = pd.read_excel('UrunListesi.xlsx')

# Tarihleri çıkar
date_pattern = r'(\d{1,2}\.\d{1,2}\.\d{4})'

# "AramaTerimleri" sütunundaki tarihleri temizle
df_calisma_alani['AramaTerimleri'] = df_calisma_alani['AramaTerimleri'].apply(lambda x: re.search(date_pattern, str(x)).group(1) if re.search(date_pattern, str(x)) else None)

# Exceli Kaydet
with pd.ExcelWriter('UrunListesi.xlsx', engine='xlsxwriter') as writer:
    df_calisma_alani.to_excel(writer, index=False, sheet_name='Sheet1')

print(Fore.YELLOW + "Ürünlerin Resim Yüklenme Tarihleri Ayrıştırıldı")
#endregion

# Excel dosyasını oku
df = pd.read_excel('UrunListesi.xlsx')

# "AramaTerimleri" sütununda dolu olan hücreleri içeren satırları bulun
dolu_sutun = df['AramaTerimleri'].notna()

# Bu satırları sil
df = df[~dolu_sutun]

# Düzenlenmiş DataFrame'i aynı dosyaya kaydet
df.to_excel('UrunListesi.xlsx', index=False)




# Excel dosyasını oku
df = pd.read_excel('UrunListesi.xlsx')

# Tekrarlayan satırları kaldır
df = df.drop_duplicates()

# Düzenlenmiş DataFrame'i aynı dosyaya kaydet
df.to_excel('UrunListesi.xlsx', index=False)
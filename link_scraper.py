# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# headlessモードでブラウザを起動（ブラウザのGUIを表示しない）
options = Options()
options.add_argument('--headless')

# WebDriverのセットアップ
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# スクレイピングしたいWebページのURL
url = 'https://workshops.aws/'
driver.get(url)

# JavaScriptが完全に読み込まれるまで待機する場合、時間を指定して待つ
driver.implicitly_wait(10)

# <a>タグを全て取得し、それぞれのhref属性（リンク先URL）を抽出
links = driver.find_elements(By.TAG_NAME, 'a')
all_links = [link.get_attribute('href') for link in links if link.get_attribute('href')]

# リンク先のURLをファイルに保存
with open('links.txt', 'w', encoding='utf-8') as file:
    for href in all_links:
        file.write(href + '\n')

# ブラウザを閉じる
driver.quit()

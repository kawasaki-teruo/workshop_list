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

# ページの全てのテキストを取得
page_text = driver.find_element(By.TAG_NAME, 'body').text

# 結果をファイルに保存
with open('page_content.txt', 'w', encoding='utf-8') as file:
    file.write(page_text)

# ブラウザを閉じる
driver.quit()

# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import json

def get_list(list1):
    return list1['url']

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

#mat-card-actions
# <a>タグを全て取得し、それぞれのhref属性（リンク先URL）とテキストを抽出
cards = driver.find_elements(By.TAG_NAME, 'aws-workshop-card')
link_details = [(card.find_element(By.CLASS_NAME, 'mat-headline').text, 
                 card.find_element(By.TAG_NAME, 'mat-card-actions').find_element(By.TAG_NAME, 'a').get_attribute('href'),
                 card.find_elements(By.TAG_NAME, 'a'),
                 card.text
                 )
                 for card in cards]

#d = {}
list1 = []
for title, href, links, text in link_details:
    href = re.sub('\n','',href)
    href = re.sub('/en-US/*$','',href)
    href = re.sub('/ja-JP/*$','',href)
    href = re.sub('/*$','',href)

    pattern1='Level: (\d\d\d)'
    res1 = re.search(pattern1, text)
    level = res1.group(1)

    pattern2='Categories: (.+)'
    res2 = re.search(pattern2, text)
    categories = [x.strip() for x in res2.group(1).split(',')]

    pattern3='Tags: (.+)'
    res3 = re.search(pattern3, text)
    tags = [x.strip() for x in res3.group(1).split(',')]

    line = text.split('\n')
    schedule = line[7].strip()
    description = line[8].strip()

    list1.append(
        {
            "url": href,
            "title": title,
            "level": level,
            "categories": categories,
            "tags": tags,
            "schedule": schedule,
            "description": description
        }
    )

#sorted_keys = sorted(d)
#sorted_dict_by_key = {k: d[k] for k in sorted_keys}
sorted_list = sorted(list1 , key=get_list , reverse=False)

# リンク先のURLとリンクテキストをファイルに保存
with open('workshop_list3.json', 'w', encoding='utf-8') as file:
    #json.dump(sorted_dict_by_key, file, ensure_ascii=False, indent=2)
    json.dump(sorted_list, file, ensure_ascii=False, indent=2)

# ブラウザを閉じる
driver.quit()


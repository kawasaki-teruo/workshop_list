from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json
import sys
import time
import psutil
import traceback


def get_list(list1):
    return list1['url']

def checkURL(url):
    try:
        print(url)
        with (webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver2):
            # ページアクセス
            driver2.get(url)
            # ページが完全にロードされるまで待機
            #driver2.implicitly_wait(30)
            time.sleep(5)
            #WebDriverWait(driver2, 20).until(EC.none_of(EC.visibility_of_all_elements_located((By.XPATH,"//body/descendant::*[contains(text(),'Loading')]"))))
            #WebDriverWait(driver2, 20).until(EC.none_of(WebDriverWait(driver2, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//body/descendant::*[contains(text(),'Loading')]")))))

            page_text = driver2.find_element(By.TAG_NAME, 'body').text
            pattern_result = re.search("Page not found", page_text)
            #print(driver2.title)
            #print(driver2.page_source)
            #print(page_text)
            #print(pattern_result)
            driver2.quit()
    except Exception as e:
        pattern_result = "Error"
        print('error1')
        print(e)
        print(type(e))

    print(pattern_result)
    if pattern_result:
        # Page not found の場合
        return False
    else:
        return True

# headlessモードでブラウザを起動（ブラウザのGUIを表示しない）
options = Options()
options.add_argument('--headless')

# WebDriverのセットアップ
try:
    with (webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver):
        
        """
        print('start11')
        href='https://catalog.us-east-1.prod.workshops.aws/workshops/e0495073-29eb-4a62-9cab-114511462198'
        valid_url = checkURL(href)
        print(valid_url)
        """

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

        list1 = []
        for title, href, links, text in link_details:
            try:
                href = re.sub('\n','',href)
                href = re.sub('/en-US/*$','',href)
                href = re.sub('/ja-JP/*$','',href)
                href = re.sub('/*$','',href)

                # Level の抽出
                pattern1='Level: (\d\d\d)'
                res1 = re.search(pattern1, text)
                if res1:
                    level = res1.group(1)
                else:
                    print(f"Warning: Level not found for '{title}'")
                    level = "000"  # デフォルト値

                # Categories の抽出
                pattern2='Categories: (.+)'
                res2 = re.search(pattern2, text)
                if res2:
                    categories = [x.strip() for x in res2.group(1).split(',')]
                else:
                    print(f"Warning: Categories not found for '{title}'")
                    categories = []  # デフォルト値

                # Tags の抽出
                pattern3='Tags: (.+)'
                res3 = re.search(pattern3, text)
                if res3:
                    tags = [x.strip() for x in res3.group(1).split(',')]
                else:
                    print(f"Warning: Tags not found for '{title}'")
                    tags = []  # デフォルト値

                line = text.split('\n')
                
                # schedule と description の安全な取得
                if len(line) > 7:
                    schedule = line[7].strip()
                else:
                    print(f"Warning: Schedule not found for '{title}'")
                    schedule = ""
                    
                if len(line) > 8:
                    description = line[8].strip()
                else:
                    print(f"Warning: Description not found for '{title}'")
                    description = ""

                valid_url = checkURL(href)
                
                list1.append(
                    {
                        "url": href,
                        "valid_url": valid_url,
                        "title": title,
                        "level": level,
                        "categories": categories,
                        "tags": tags,
                        "schedule": schedule,
                        "description": description
                    }
                )
            except Exception as e:
                print(f"Error processing card: {title}")
                print(f"Error: {e}")
                print(f"Card text: {text}")
                print(traceback.format_exc())
                # エラーが発生してもスキップして続行
                continue

        sorted_list = sorted(list1 , key=get_list , reverse=False)

        # リンク先のURLとリンクテキストをファイルに保存
        with open('workshop_list4.json', 'w', encoding='utf-8') as file:
            json.dump(sorted_list, file, ensure_ascii=False, indent=2)

        # ブラウザを閉じる
        #driver.quit()

except Exception as e:
    print(e)
    print(type(e))
    print(traceback.format_exc())

exists_chromedriver = False
for proc in psutil.process_iter():
    if proc.name() == "chromedriver":
        print(proc)
        exists_chromedriver = True
        break

if exists_chromedriver:
    print("chromedriver プロセスが存在します。")
else:
    print("chromedriver プロセスが存在しません。")
sys.exit()

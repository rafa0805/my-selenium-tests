# import os

# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# driver = webdriver.Remote(
#     # command_executor=os.environ["SELENIUM_URL"],
#     command_executor="http://docker-chrome-1:4444/wd/hub",
#     desired_capabilities=DesiredCapabilities.FIREFOX.copy()
# )
# driver.implicitly_wait(5)

# driver.get("https://www.time-j.net/worldtime/country/jp")

# print(driver.find_element_by_xpath("/html/body/div/div[6]/div[1]/div/p[5]").text)
# driver.quit()

#!/usr/bin/python3

from selenium import webdriver
import time

# Chromeのオプション
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Selenium Serverに接続
driver = webdriver.Remote(command_executor='http://docker-chrome-1:4444/wd/hub',
options=options)

try:
  # 要素の待機時間を最大10秒に設定
  driver.implicitly_wait(10)

  # https://gihyo.jp を開く
  driver.get('https://gihyo.jp')

  # 検索ボックスに「Ubuntu」を入力
  element_search_form = driver.find_element_by_id('searchFormKeyword')
  element_search_form.send_keys('Ubuntu')

  # 検索ボタンをクリック
  element_search_button = driver.find_element_by_id('searchFormSubmit')
  element_search_button.click()
  time.sleep(5)

  # 検索結果のタイトルを取得して出力
  element_titles = driver.find_elements_by_xpath("//a[@class='gs-title']")
  for element_title in element_titles:
    if not element_title.text.strip():
      continue
    print(element_title.text.strip())

except:
  import traceback
  traceback.print_exc()

finally:
  # Chromeを終了
  input("何かキーを押すと終了します...")
  driver.quit()
import pytest
import time
import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# = = = = = Cheet Sheets = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
#  ***** 要素の取得構文例 *****
#  self.driver.find_element(By.TAG_NAME, "example") ----- タグ名で要素を取得
#  self.driver.find_element(By.ID, "example") ----- id属性値で要素を取得
#  self.driver.find_element(By.NAME, "example") ----- name属性値で要素を取得
#  self.driver.find_element(By.CSS_SELECTOR, "example") ----- cssのセレクタ表記で要素を取得
#  self.driver.find_element(By.XPATH, "example") ----- XPathで要素を取得
#  self.driver.find_element(By.LINK_TEXT, "example") ----- アンカーのテキストによって要素を取得
#  self.driver.find_element(By.PARTIAL_LINK_TEXT, "example") ----- アンカーの部分テキストによって要素を取得

#  ***** 状態評価の構文例 *****
#  .is_enabled() ----- 要素がアクティブかを評価
#  .isSelected() ----- 要素が選択されているかを評価 (チェックボックスやラジオボタン)
#  .send_keys("example") ----- 取得した要素に値を入力する
#  .click() ----- 取得した要素をクリックする

#  ***** セレクトタグの選択方法 *****
#  方法①
#  dropdown = self.driver.find_element(By.ID, "example_select")
#  dropdown.find_element(By.XPATH, "//option[. = 'example_option']").click()
#  方法②
#  select_element = driver.find_element(By.ID,'example_select')
#  select_object = Select(select_element)
#  select_object.select_by_index(1)
#  select_object.select_by_value('example')
#  select_object.select_by_visible_text('example')

#  ***** 要素のパラメータを取得する構文例 *****
#  .tag_name ----- 要素のタグの種類を取得
#  .text ----- 要素のテキストを取得
#  .title ----- ページのタイトルを取得を取得 (要素ではなくドライバーオブジェクトに対して使う)
#  .rect ----- 親要素の左上を基準にした、要素のx座標、y座標 & 高さ、幅を取得
#  .value_of_css_property('color') ----- 要素のcssのプロパティの値を取得 (例文はcolorプロパティの値を取得)

#  ***** 非同期処理を待機する例 *****
#  WebDriverWait(self.driver, 30000).until(expected_conditions.text_to_be_present_in_element((By.LINK_TEXT, "example"), "example_text"))

# = = = = = Cheet Sheets = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 

class WebTest():

  # *************** Class Interface ***************
  def __init__(self, cases, browser, output="./output/"):
    # set params
    self.cases = cases
    self.browser = browser
    self.output_path = output
    # set up dirs
    self.create_output_dirs()
    # start up driver
    self.start_driver(self.browser)
    # evaluation params
    self.true_n = 0
    self.false_n = 0
    self.assessment_n = 0
    self.case_true_n = 0
    self.case_false_n = 0
    self.case_assessment_n = 0
    self.summary = list()

  def execute(self):
    count = 0
    last_flag = 0
    for case in self.cases:
      count += 1
      if count == len(self.cases):
        last_flag = 1
      self.flow(case, last_flag)

  def teardown_method(self, method):
    self.driver.quit()

  def create_output_dirs(self):
    os.makedirs(self.output_path + "screenshots/", mode=0o777, exist_ok=True)
    os.makedirs(self.output_path + "logs/", mode=0o777, exist_ok=True)
 


  # *************** Main Process ***************
  def flow(self, case, last_flag):

    self.driver.get("https://www.youtube.com/")
    exit()
    self.driver.find_element(By.ID, "session_email").send_keys(case["session_email"])
    self.driver.find_element(By.ID, "session_password").send_keys(case["session_password"])

    element = self.driver.find_elements(By.ID, "flash")
    self.count_assess_result(bool(len(element) > 0))
    
    time.sleep(1)
    filename = self.output_path + "screenshots/" + self.browser + "_" + case["case_name"] + "_a"
    self.full_screen(filename)

    self.show_summary(case['case_name'])

    if last_flag == 1:
      self.driver.close()
      self.driver.quit()
    else:
      self.driver.refresh()



  # *************** Evaluate ***************
  def show_summary(self, casename):
    result = {
      'case_name' : casename,
      'case_assessment_n' : self.case_assessment_n,
      'case_true_n' : self.case_true_n,
      'case_false_n' : self.case_false_n
    }
    self.summary.append(result)
    self.reset_count()

  def count_assess_result(self, result):
    self.assessment_n += 1
    self.case_assessment_n += 1
    if result:
      self.true_n += 1
      self.case_true_n += 1
    else:
      self.false_n += 1
      self.case_false_n += 1
  
  def reset_count(self):
    self.case_true_n = 0
    self.case_false_n = 0
    self.case_assessment_n = 0



  # *************** Utilities ***************
  def full_screen(self, filename):
    w = self.driver.execute_script("return document.body.scrollWidth")
    h = self.driver.execute_script("return document.body.scrollHeight")
    self.driver.set_window_size(w, h)
    self.driver.save_screenshot(filename + ".png")



  # *************** Setting up Drivers ***************
  def start_driver(self, browser):
    if browser == "Firefox":
      self.firefox_driver()
    elif browser == "Chrome":
      self.chrome_driver()
    elif browser == "IE":
      self.ie_driver()
    elif browser == "Edge":
      self.edge_driver()
    elif browser == "Safari":
      self.safari_driver()
    else:
      print("pleas select a browser")
      exit()

  def chrome_driver(self):
    from selenium.webdriver.chrome.options import Options
    self.options = Options()
    self.options.add_argument('--headless')
    self.driver = webdriver.Chrome(options=self.options)

  def firefox_driver(self):
    from selenium.webdriver.firefox.options import Options
    options = Options()
    # path for default profiles can be found in your brouser by putting "about:profiles" on search box
    profile = webdriver.FirefoxProfile(r"xxxxx")
    # options.add_argument('-headless')
    self.driver = webdriver.Firefox(firefox_options=options, firefox_profile=profile ,log_path=self.output_path + "logs/geckodriver.log")

  def edge_driver(self):
    # from selenium.webdriver.edge.options import Options
    from msedge.selenium_tools import Edge, EdgeOptions
    self.options = EdgeOptions()
    self.options.use_chromium = True

    # self.options.add_argument('--headless')
    self.driver = Edge(options=self.options)

  def safari_driver(self):
    print("comming soon...")
    exit()

  def ie_driver(self):
    from selenium.webdriver.ie.options import Options
    self.options = Options()
    self.driver = webdriver.Ie()
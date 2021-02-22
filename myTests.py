import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 

class WebTest():

  # *************** クラスインタフェース ***************
  def __init__(self, cases, browser):
    self.cases = cases
    self.browser = browser
    self.start_driver(self.browser)
    self.save_path = "./screenshots/"

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
 


  # *************** メイン処理 ***************
  def flow(self, case, last_flag):
    self.driver.get("https://www.astomos-retailing.com/order/")
    self.driver.find_element(By.ID, "campaign_code").send_keys(case["campaign_code"])
    self.driver.find_element(By.ID, "name_sei").send_keys(case["name_sei"])
    self.driver.find_element(By.ID, "name_mei").send_keys(case["name_mei"])
    self.driver.find_element(By.ID, "customer_code1").send_keys(case["customer_code1"])
    self.driver.find_element(By.ID, "customer_code2").send_keys(case["customer_code2"])
    self.driver.find_element(By.ID, "customer_code3").send_keys(case["customer_code3"])
    self.driver.find_element(By.ID, "zip1").send_keys(case["zip1"])
    self.driver.find_element(By.ID, "zip2").send_keys(case["zip2"])
    time.sleep(1)    
    self.full_screen(self.save_path + self.browser + "_" + case["case_name"] + "_a")

    if last_flag == 1:
      self.driver.close()
      self.driver.quit()
    else:
      self.driver.refresh()



  # *************** 小分け関数群 ***************
  def full_screen(self, filename):
    w = self.driver.execute_script("return document.body.scrollWidth")
    h = self.driver.execute_script("return document.body.scrollHeight")
    self.driver.set_window_size(w, h)
    self.driver.save_screenshot(filename + ".png")



  # *************** ドライバ関連の関数群 ***************
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
    self.options = Options()
    self.options.add_argument('-headless')
    self.driver = webdriver.Firefox(firefox_options=self.options)

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
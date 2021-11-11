# import pytest
import time
import json
import os
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait 

class WebTest():

  # *************** Class Interface ***************
  def __init__(self, cases, browser, output="./output_20210415/"):
    # set params
    self.cases = cases
    self.browser = browser
    self.output_path = output
    # set up dirs
    self.create_output_dirs()
    # start up driver
    self.start_driver(self.browser)
    # evaluation params
    self.true_num = 0
    self.false_num = 0
    self.assessment_num = 0
    self.case_true_num = 0
    self.case_false_num = 0
    self.case_assessment_num = 0
    self.summary = list()

  def execute(self):
    count = 0
    last_flag = 0

    for case in self.cases:
      count += 1

      if count == len(self.cases):
        last_flag = 1

      self.test_flow(case, last_flag)

  def teardown_method(self, method):
    self.driver.quit()
 


  # *************** Main Process ***************
  def test_flow(self, case, last_flag):

    self.driver.get(case["url"])
    
    if case["no"] == "1":
      # self.driver.find_element(By.ID, "name").send_keys("kinosita@bp-net.co.jp")
      self.driver.find_element(By.ID, "password").send_keys("bp202!sf")
      self.driver.find_element(By.ID, "Login").click()

    time.sleep(15)

    filename = self.output_path + "screenshots/" + case["case_name"]
    self.full_screen(filename)

    data = self.extract_element()
    for i in range(len(data)):
      self.driver.get("https://est-pro.lightning.force.com" + data[i][-1])
      
      time.sleep(5)

      filename = self.output_path + "screenshots/details/" + case["case_name"] + "_" + str(i)
      self.full_screen_original(filename)

    print(data)

    f = open(self.output_path + "extracts/" + case["case_name"] + ".csv", 'w', encoding='utf-8', newline='')
    dataWriter = csv.writer(f)
    for i in range(len(data)):
      dataWriter.writerow(data[i])
    f.close()

    self.show_summary(case['case_name'])



  # *************** Evaluate ***************
  def show_summary(self, casename):
    result = {
      'case_name' : casename,
      'case_assessment_num' : self.case_assessment_num,
      'case_true_num' : self.case_true_num,
      'case_false_num' : self.case_false_num
    }
    self.summary.append(result)
    self.reset_count()

  def count_assess_result(self, result):
    self.assessment_num += 1
    self.case_assessment_num += 1
    if result:
      self.true_num += 1
      self.case_true_num += 1
    else:
      self.false_num += 1
      self.case_false_num += 1
  
  def reset_count(self):
    self.case_true_num = 0
    self.case_false_num = 0
    self.case_assessment_num = 0



  # *************** Utilities ***************
  def full_screen(self, filename):
    # w = self.driver.execute_script("return document.body.scrollWidth")
    # h = self.driver.execute_script("return document.body.scrollHeight")
    h = self.driver.execute_script("return document.getElementsByClassName('scroller')[1].scrollHeight")
    self.driver.set_window_size(1899, h + 1000)
    time.sleep(10)

    while (self.driver.execute_script("return document.getElementsByClassName('scroller')[1].scrollHeight") != h):
      h = self.driver.execute_script("return document.getElementsByClassName('scroller')[1].scrollHeight")
      self.driver.set_window_size(1899, h + 1000)
      time.sleep(10)

    time.sleep(10)
    self.driver.save_screenshot(filename + ".png")

  def full_screen_original(self, filename):
    w = 1520
    h = 2000
    # w = self.driver.execute_script("return document.body.scrollWidth")
    # h = self.driver.execute_script("return document.body.scrollHeight")
    self.driver.set_window_size(w, h)
    time.sleep(10)
    self.driver.save_screenshot(filename + ".png")

  def create_output_dirs(self):
    os.makedirs(self.output_path + "screenshots/", mode=0o777, exist_ok=True)
    os.makedirs(self.output_path + "extracts/", mode=0o777, exist_ok=True)
    os.makedirs(self.output_path + "logs/", mode=0o777, exist_ok=True)

  def extract_element(self):
    script = """
    let data = new Array;
    let lines = document.querySelectorAll('.slds-table tbody tr');
    let links = document.querySelectorAll('.slds-table tbody tr a:not(.rowActionsPlaceHolder)');
    lines.forEach(function(tr, i) {
      data[i] = new Array;
      for (let j = 0; j < tr.cells.length; j ++) {
        data[i].push(tr.cells[j].textContent);
      }
      data[i].push(links[i].getAttribute('href'));
    });
    return data;
    """
    return self.driver.execute_script(script)

  # def extract_text(self):
  #   script = """
  #   let frame = document.querySelectorAll('iframe[title="*契約 カスタム項目: *お客様最終更新日 ~ Salesforce - Enterprise Edition"]');
  #   let target = document.querySelectorAll('tr.last.detailRow');
  #   let text;
  #   if (target.length == 1) {
  #     text = target.textContent;
  #   } else {
  #     text = target.length;
  #   }
  #   return text;
  #   """
  #   return self.driver.execute_script(script)



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
    profile = webdriver.FirefoxProfile(r"C:\\Users\\best201911\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xabd6x81.default-release")
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
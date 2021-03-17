# import pytest
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

    self.driver.get("https://www.selenium.dev/")

    element = self.driver.find_elements(By.ID, "flash")
    self.count_assess_result(bool(len(element) > 0))
    
    filename = self.output_path + "screenshots/" + self.browser + "_" + case["case_name"] + "_write_what_u_want"
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
    w = self.driver.execute_script("return document.body.scrollWidth")
    h = self.driver.execute_script("return document.body.scrollHeight")
    self.driver.set_window_size(w, h)
    self.driver.save_screenshot(filename + ".png")

  def create_output_dirs(self):
    os.makedirs(self.output_path + "screenshots/", mode=0o777, exist_ok=True)
    os.makedirs(self.output_path + "logs/", mode=0o777, exist_ok=True)



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
    profile = webdriver.FirefoxProfile(r"C:\\Users\\RAFAEL\\Documents\\MyBookShelf\\Repositories\\my-selenium\\config\\profiles")
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
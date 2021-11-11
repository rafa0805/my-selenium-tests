import time
import random

# Selenium modules
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Original Modules
from src.MyBrowserFactory import MyBrowserFactory
from src.MyUiTest import MyUiTest

class MyLacocoFormUiTest(MyUiTest):

  def __init__(self, output="./output/ui_test"):
    super().__init__(output)

  def exec_test(self):
    self.test_case()

  def test_case(self):
    self.step1()
    self.step2()

  def step1(self):
    # Open the page
    self.browser.driver.get('https://form.la-coco.com/yoyaku/index.html')

    # Page 1
    select_element = self.browser.driver.find_element(By.CSS_SELECTOR, ".address_list")
    select_object = Select(select_element)
    random_prefecture_index = random.choice(range(1, len(select_object.options) - 1))
    select_object.select_by_index(random_prefecture_index)

    w = self.browser.driver.execute_script("return document.body.scrollWidth")
    h = self.browser.driver.execute_script("return document.getElementsByClassName('site_wrapper')[0].scrollHeight")
    self.browser.driver.set_window_size(w, h + 1000)
    time.sleep(2)

    shop_elements = self.browser.driver.find_elements(By.CSS_SELECTOR, ".form-shop-list .form-shop-item")
    if len(shop_elements) == 1:
      random_shop_index = 0
    else:
      random_shop_index = random.choice(range(0, len(shop_elements) - 1))

    shop_elements[random_shop_index].click()

    # time.sleep(5)
    # w = self.browser.driver.execute_script("return document.body.scrollWidth")
    # h = self.browser.driver.execute_script("return document.getElementsByClassName('site_wrapper')[0].scrollHeight")
    # self.browser.driver.set_window_size(w, h + 1000)
    # time.sleep(2)

    WebDriverWait(self.browser.driver, 30000).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".cal_next .cal-button")))

    # for i in range(3):
    #   next_button = self.browser.driver.find_element(By.CSS_SELECTOR, ".cal_next .cal-button")
    #   next_button.click()

    #   if i < 2:
    #     WebDriverWait(self.browser.driver, 30000).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".cal_next .cal-button")))

    found_flag = False
    cal_cell_elements = self.browser.driver.find_elements(By.CSS_SELECTOR, ".cal-cell.free")
    last_cal_cell_available = cal_cell_elements[len(cal_cell_elements) - 1]

    last_cal_cell_available.click()


    # 3回次の週へを押す
    # ●のものがあれば、その最後の要素をクリック
    # なければ店舗を選びなおす

    # Screen shot
    self.browser.unknown_size_full_screen_shot('./test')

    next_page_button = self.browser.driver.find_element(By.CSS_SELECTOR, ".a__button")
    next_page_button.click()

  def step2(self):
    WebDriverWait(self.browser.driver, 30000).until(expected_conditions.visibility_of_element_located((By.ID, "name_sei")))

    name_sei = self.browser.driver.find_element(By.ID, "name_sei")
    name_sei.send_keys("テスト")
    
    given_name = self.browser.driver.find_element(By.ID, "given-name")
    given_name.send_keys("テスト")

    kana_sei = self.browser.driver.find_element(By.ID, "kana_sei")
    kana_sei.send_keys("テスト")

    kana_mei = self.browser.driver.find_element(By.ID, "kana_mei")
    kana_mei.send_keys("テスト")

    tel = self.browser.driver.find_element(By.ID, "tel")
    tel.send_keys("08011112222") #ddhhmmssにすればかぶらん

    email = self.browser.driver.find_element(By.ID, "email")
    email.send_keys("kosaka@bp-net.co.jp")

    w = self.browser.driver.execute_script("return document.body.scrollWidth")
    h = self.browser.driver.execute_script("return document.getElementsByClassName('site_wrapper')[0].scrollHeight")
    self.browser.driver.set_window_size(w, h + 1000)
    time.sleep(2)

    policy_button =  self.browser.driver.find_element(By.CSS_SELECTOR, ".form-policy-input input[type=checkbox]")
    policy_button.click()

    # Screen shot
    self.browser.unknown_size_full_screen_shot('./test')

    next_page_button = self.browser.driver.find_element(By.CSS_SELECTOR, ".a__button")
    next_page_button.click()


    # 画面サイズを調整する関数を作る
    # セレクトをランダムに選択するメソッドを作る
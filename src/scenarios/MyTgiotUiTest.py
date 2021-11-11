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

class MyTgiotUiTest(MyUiTest):

  def __init__(self, output="./output/ui_test"):
    super().__init__(output)
    # シミュレーションをスキップするリスト
    self.skipSimulationList = ["新築", "ふるさと"]

  def exec_test(self, params):
    self.test_case(params)

  def test_case(self, params):
    # メール疎通で取得するトークンが未設定なら前半処理を、設定済なら後半処理を実行する
    if "token" in params and params["token"] == "":
      self.simulation(params)
      self.mail(params)
      self.mailsend(params)
    else:
      self.select(params)
      self.input(params)
      self.confirm(params)
      self.complete(params) # cleanup
      
    self.browser.terminate() # cleanup

  def simulation(self, params):
    # Open the page
    self.browser.driver.get(params["case_url_path"])

    if (params["form_type"] not in self.skipSimulationList):
      # サービス種別の選択
      if params["services"] == "ガス+IoT":
        self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='services_1004000001']").click()
      elif params["services"] == "IoTのみ":
        self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='services_1004000002']").click()
      else:
        print("Error: 不正なサービス種別です。")
        exit
      
      # センサー個数入力
      self.browser.driver.find_element(By.ID, "services_2103010001").send_keys(params["services_2103010001"])
      self.browser.driver.find_element(By.ID, "services_2103010003").send_keys(params["services_2103010003"])
      self.browser.driver.find_element(By.ID, "services_2103010002").send_keys(params["services_2103010002"])

      # 支払い方法選択
      select_element = self.browser.driver.find_element(By.ID,'pay_month')
      select_object = webdriver.support.select.Select(select_element)
      select_object.select_by_visible_text(params["pay_month"])
      select_element = self.browser.driver.find_element(By.ID,'pay_initial')
      select_object = webdriver.support.select.Select(select_element)
      select_object.select_by_visible_text(params["pay_initial"])

      # シミュレーション結果が表示されるまで待機
      WebDriverWait(self.browser.driver, 30000).until(expected_conditions.visibility_of_element_located((By.ID, "simulation_result")))
      time.sleep(1)
    
      # フルスクリーンショットの取得
      filename = self.screenshot_dir + "/" + params["case_name"] + "_step1(シミュレーション画面)"
      self.browser.full_screen_shot(filename)

      # Next page
      self.browser.driver.find_element(By.CSS_SELECTOR, "button[name='submit_btn']").click()
    else:
      return

  def mail(self, params):
    WebDriverWait(self.browser.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']")))
    time.sleep(3)

    # メールアドレス入力
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='email']").send_keys(params["email"])

    # フルスクリーンショットの取得
    filename = self.screenshot_dir + "/" + params["case_name"] + "_step2(メール送信画面)"
    self.browser.full_screen_shot(filename)

    # Next page
    self.browser.driver.find_element(By.CSS_SELECTOR, "button[name='submit_btn']").click()
    time.sleep(5)
    return

  def mailsend(self, params):
    # フルスクリーンショットの取得
    filename = self.screenshot_dir + "/" + params["case_name"] + "_step3(メール送信済み画面)"
    self.browser.full_screen_shot(filename)

  def select(self, params):
    self.browser.driver.get("https://tgiot.bp-task.com/order/select.html" + params["token"])
    # WebDriverWait(self.browser.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "a.mail")))
    time.sleep(5)
    self.browser.driver.find_element(By.CSS_SELECTOR, "a.mail").click()

  def input(self, params):
    # シミュレーション結果が描画されるまで待機
    time.sleep(5)

    # 利用場所区分のせんたく処理
    select_element = self.browser.driver.find_element(By.ID,'place_name')
    select_object = webdriver.support.select.Select(select_element)
    select_object.select_by_visible_text(params["place_name"])
    if params["place_name"] == "その他":
      self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='place_name_other']").send_keys(params["place_name_other"])
    
    # 個人情報入力
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='zip_1']").send_keys(params["zip_1"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='zip_2']").send_keys(params["zip_2"])
    time.sleep(3)
    # self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='address']").send_keys(params["address"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='address_4_1']").send_keys(params["address_4_1"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='address_4_2']").send_keys(params["address_4_2"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='address_5']").send_keys(params["address_5"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='address_6_1']").send_keys(params["address_6_1"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='address_6_2']").send_keys(params["address_6_2"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='customer_no']").send_keys(params["customer_no"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='name_sei']").send_keys(params["name_sei"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='name_mei']").send_keys(params["name_mei"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='kana_sei']").send_keys(params["kana_sei"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='kana_mei']").send_keys(params["kana_mei"])
    select_element = self.browser.driver.find_element(By.ID,'birth_y')
    select_object = webdriver.support.select.Select(select_element)
    select_object.select_by_visible_text(params["birth_y"] + "年")
    select_element = self.browser.driver.find_element(By.ID,'birth_m')
    select_object = webdriver.support.select.Select(select_element)
    select_object.select_by_visible_text(params["birth_m"] + "月")
    select_element = self.browser.driver.find_element(By.ID,'birth_d')
    select_object = webdriver.support.select.Select(select_element)
    select_object.select_by_visible_text(params["birth_d"] + "日")
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='tel_1']").send_keys(params["tel_1"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='tel_2']").send_keys(params["tel_2"])
    self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='tel_3']").send_keys(params["tel_3"])
    if params["sex"] == "男":
      self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='sex_1']").click()
    elif params["sex"] == "女":
      self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='sex_2']").click()
    elif params["sex"] == "その他":
      self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='sex_3']").click()
    else:
      print("Error: 不正な性別です。")

    # 非簡略パターン
    if ( params["form_type"] not in self.skipSimulationList ) :
      #  本人との関係を選択する
      select_element = self.browser.driver.find_element(By.ID,'relation')
      select_object = webdriver.support.select.Select(select_element)
      select_object.select_by_visible_text(params["relation"])
      if params["relation"] == "その他":
        self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='relation_other']").send_keys(params["relation_other"])
      
      if params["relation"] != "本人":
        # 契約者の個人情報の入力
        self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='contructor_sei']").send_keys(params["contructor_sei"])
        self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='contructor_mei']").send_keys(params["contructor_mei"])
        self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='contructor_kana_sei']").send_keys(params["contructor_kana_sei"])
        self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='contructor_kana_mei']").send_keys(params["contructor_kana_mei"])
        select_element = self.browser.driver.find_element(By.ID,'contractor_birth_y')
        select_object = webdriver.support.select.Select(select_element)
        select_object.select_by_visible_text(params["contractor_birth_y"] + "年")
        select_element = self.browser.driver.find_element(By.ID,'contractor_birth_m')
        select_object = webdriver.support.select.Select(select_element)
        select_object.select_by_visible_text(params["contractor_birth_m"] + "月")
        select_element = self.browser.driver.find_element(By.ID,'contractor_birth_d')
        select_object = webdriver.support.select.Select(select_element)
        select_object.select_by_visible_text(params["contractor_birth_d"] + "日")
        self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='contructor_tel_1']").send_keys(params["contructor_tel_1"])
        self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='contructor_tel_2']").send_keys(params["contructor_tel_2"])
        self.browser.driver.find_element(By.CSS_SELECTOR, "input[name='contructor_tel_3']").send_keys(params["contructor_tel_3"])

        # 支払い区分の選択
        if params["payer_kbn"] == "契約者":
          self.browser.driver.find_element(By.ID, "payer_kbn_1").click()
        elif params["payer_kbn"] == "申込者":
          self.browser.driver.find_element(By.ID, "payer_kbn_2").click()
        else:
          print("Error: 不正な支払い区分です。")
    
    # 連絡用情報の入力
    if (params["contact_tel_kbn"] == "契約者" and params["relation"] != "本人"):
      self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='contact_tel_kbn_1']").click()
    elif params["contact_tel_kbn"] == "申込者":
      self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='contact_tel_kbn_2']").click()
    elif params["contact_tel_kbn"] == "その他":
      self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='contact_tel_kbn_9']").click()
      self.browser.driver.find_element(By.ID, "contact_tel_1").send_keys(params["contact_tel_1"])
      self.browser.driver.find_element(By.ID, "contact_tel_2").send_keys(params["contact_tel_2"])
      self.browser.driver.find_element(By.ID, "contact_tel_3").send_keys(params["contact_tel_3"])
      select_element = self.browser.driver.find_element(By.ID,'contact_time')
      select_object = webdriver.support.select.Select(select_element)
      select_object.select_by_visible_text(params["contact_time"])
    else:
      print("Error: 不正な連絡先区分です。")

    if params["form_type"] != "ふるさと":
      # サービス説明希望
      if params["service_kbn"] == "無":
        self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='service_kbn_0']").click()
      elif params["service_kbn"] == "有":
        self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='service_kbn_1']").click()
      else:
        print("Error: 不正な入力です。(サービス説明)")

      # 利用せびの選択
      if params["facility"] == "なし":
        self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='facility_0']").click()
      elif params["facility"] == "エネファーム":
        self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='facility_1']").click()
      elif params["facility"] == "エコウィル":
        self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='facility_2']").click()
      elif params["facility"] == "ガスヒートポンプ":
        self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='facility_3']").click()
      else:
        print("Error: 不正な入力です。(利用設備)")

      # 紹介者コード入力
      self.browser.driver.find_element(By.ID, "referral_cd").send_keys(params["referral_cd"])
    
      # かけつけ希望
      if params["kaketuke_kibo"] == "希望あり":
        self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='kaketuke_kibo_1']").click()
      elif params["kaketuke_kibo"] == "希望なし":
        self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='kaketuke_kibo_2']").click()
      else:
        print("Error: 不正な入力です。(かけつけ希望)")

    # 利用規約の確認ボタンを有効化してクリック
    self.browser.driver.execute_script("$('#agree_service').prop('disabled', false).parents('div:first').removeClass('invalid');")
    self.browser.driver.find_element(By.CSS_SELECTOR, "label[for='agree_service']").click()

    # フルスクリーンショットの取得
    filename = self.screenshot_dir + "/" + params["case_name"] + "_step5(入力画面)"
    self.browser.full_screen_shot(filename)

    # Next page
    self.browser.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

  def confirm(self, params):
    time.sleep(2)
    # フルスクリーンショットの取得
    filename = self.screenshot_dir + "/" + params["case_name"] + "_step6(確認顔面)"
    self.browser.full_screen_shot(filename)

    # Next page
    self.browser.driver.find_element(By.CSS_SELECTOR, "#page_confirm button[type='submit']").click()


    # self.driver.set_window_size(1080, 800)
    # time.sleep(3)
    # # button = self.driver.find_element(By.CSS_SELECTOR, "button[name='submit_btn']")
    # # self.scrollByElemAndOffset(button)
    # self.driver.execute_script("document.getElementById('footer-nav-secondary-list').scrollIntoView();")
    # time.sleep(3)

    # # Next page
    # # self.driver.find_element(By.CSS_SELECTOR, "button[name='submit_btn']").click()
    # input("Press enter to continue operation...")


  def complete(self, params):
    time.sleep(2)
    # フルスクリーンショットの取得
    filename = self.screenshot_dir + "/" + params["case_name"] + "_step7(完了画面)"
    self.browser.full_screen_shot(filename)


    # 画面サイズを調整する関数を作る
    # セレクトをランダムに選択するメソッドを作る
import os
import datetime

from src.MyBrowserFactory import MyBrowserFactory

class MyUiTest():

  def __init__(self, output="./output/ui_test"):
    self.browser = MyBrowserFactory.create_browser(browser="Chrome", optionsArr=[], endPoint='docker-chrome-1')
    # set up dirs
    self.output_dir = output
    self.screenshot_dir = self.output_dir + "/results/"
    self.logs_dir = self.output_dir + "/logs"
    self.create_output_dirs()
    # evaluation params
    self.true_n = 0
    self.false_n = 0
    self.assessment_n = 0
    self.case_true_n = 0
    self.case_false_n = 0
    self.case_assessment_n = 0
    self.summary = list()

  def create_output_dirs(self):
    os.makedirs(self.output_dir, mode=0o777, exist_ok=True)
    os.makedirs(self.screenshot_dir, mode=0o777, exist_ok=True)
    os.makedirs(self.logs_dir, mode=0o777, exist_ok=True)

  def exec_test(self):
    self.test_case()

  def test_case(self):
    print("Hello World from selenium.")

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

  # 画面サイズを調整する関数を作る
  # セレクトをランダムに選択するメソッドを作る
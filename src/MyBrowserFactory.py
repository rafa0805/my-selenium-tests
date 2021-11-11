from selenium import webdriver
from src.MyBrowser import MyBrowser

class MyBrowserFactory():

  @classmethod
  def create_browser(cls, browser, optionsArr, endPoint):
    options = cls.configure(browser, optionsArr)
    return MyBrowser(endPoint=endPoint, options=options)
    # return webdriver.Chrome(options=self.options)
  
  @classmethod
  def configure(cls, browser, optionsArr):
    if browser == "Chrome":
      return cls.configure_chrome(optionsArr)
    else:
      print("no match on browser list...")

  @classmethod
  def configure_chrome(cls, optionsArr):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--headless")
    return options
  
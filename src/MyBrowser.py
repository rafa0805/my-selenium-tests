from selenium import webdriver
import time

class MyBrowser:
  def __init__(self, options, endPoint):
    try:
      self.driver = webdriver.Remote(command_executor='http://' + endPoint + ':4444/wd/hub', options=options)
    except:
      print("something went wrong when creating driver...")
  
  def full_screen_shot(self, filename):
    standard_device_w = 1920
    w = self.driver.execute_script("return document.body.scrollWidth")
    h = self.driver.execute_script("return document.body.scrollHeight")

    if standard_device_w > w:
      effective_w = standard_device_w
    else:
      effective_w = w

    effective_h = h

    self.screen_shot(filename, effective_w, effective_h)

  def screen_shot(self, filename, w, h):
    self.driver.set_window_size(w, h)
    time.sleep(10) #画面サイズ変更に伴いローディングが発生するケースがあるので
    self.driver.save_screenshot(filename + ".png")

  def unknown_size_full_screen_shot(self, filename):
    w = self.driver.execute_script("return document.body.scrollWidth")
    h = self.driver.execute_script("return document.getElementsByClassName('site_wrapper')[0].scrollHeight")
    self.driver.set_window_size(w, h + 1000)

    time.sleep(10)

    while (self.driver.execute_script("return document.getElementsByClassName('site_wrapper')[0].scrollHeight") != h):
      h = self.driver.execute_script("return document.getElementsByClassName('site_wrapper')[0].scrollHeight")
      self.driver.set_window_size(w, h + 2000)
      time.sleep(10)

    self.screen_shot(filename, w, h)


  def scrollByElemAndOffset(self, element, offset = 0):

    self.driver.execute_script("arguments[0].scrollIntoView();", element)

    if (offset != 0):
        script = "window.scrollTo(0, window.pageYOffset + " + str(offset) + ");"
        self.driver.execute_script(script)


  def terminate(self):
    self.driver.close()
    self.driver.quit()


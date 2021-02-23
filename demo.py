import myTests

browsers = [
  # "Chrome",
  "Firefox"
  # "Edge"
]

cases = [
  {"case_name" : "test1", "search" : "Selenium1"},
  {"case_name" : "test2", "search" : "Selenium2"},
  {"case_name" : "test3", "search" : "Selenium3"}
]

for browser in browsers:
  test = myTests.WebTest(cases, browser)
  test.execute()
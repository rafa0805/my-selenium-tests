import myTests

browsers = [
  # "Chrome",
  # "Firefox",
  "Edge"
]

cases = [
  {"case_name" : "case1", "campaign_code" : "132", "name_sei" : "テスト", "name_mei" : "ネーム", "customer_code1" : "1111", "customer_code2" : "222222", "customer_code3" : "3", "zip1" : "100", "zip2" : "0004"},
  {"case_name" : "case2", "campaign_code" : "132", "name_sei" : "テスト", "name_mei" : "ネーム", "customer_code1" : "1111", "customer_code2" : "222222", "customer_code3" : "3", "zip1" : "100", "zip2" : "0004"},
  {"case_name" : "case3", "campaign_code" : "132", "name_sei" : "テスト", "name_mei" : "ネーム", "customer_code1" : "1111", "customer_code2" : "222222", "customer_code3" : "3", "zip1" : "100", "zip2" : "0004"}
]

for browser in browsers:
  test = myTests.WebTest(cases, browser)
  test.execute()
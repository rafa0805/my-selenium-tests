from library import myTests, myCsv

csv = myCsv.CSV()
csv.set_csv(file="./datasample.csv", param_row=1, row_start=2, delimiter=",", encoding="shift_jis")

cases = csv.make_dict()

browsers = [
  # "Chrome",
  "Firefox"
  # "Edge"
]

dim2_array = [
  [1, 2, 3],
  [1, 2, 3],
  [1, 2, 3]
]

csv.make_csv(dim2_array)

# for browser in browsers:
#   test = myTests.WebTest(cases, browser)
#   test.execute()

#     for result in test.summary:
#     print(result)

#   datas = myTests.WebTest.extracts
#   list(datas[0].keys())
#   for data in range(len(datas)):
#     for key in data 
import myTests
import myCsv

browsers = [
  # "Chrome",
  "Firefox"
  # "Edge"
]

csv = myCsv.CSV(file="./datasample.csv", param_row="1", row_start="2", delimiter=",", encoding="shift_jis")

cases = csv.make_dictionary()

for browser in browsers:
  test = myTests.WebTest(cases, browser)
  test.execute()

  for result in test.summary:
    print(result)
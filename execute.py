import os
import datetime
import shutil

from src.MyCsv import MyCSV
from src.scenarios.MyTgiotUiTest import MyTgiotUiTest



# configuration & preparation
dt = datetime . datetime . now ( )
time_str = "{}{}{}_{}{}{}".format(str(dt.year).zfill(4), str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2), str(dt.second).zfill(2))

TEST_NAME = "tgiot_dev_20211111"
CASES_DIR = "./cases"
# OUTPUT_DIR = "./output/ui_test/" + time_str
OUTPUT_DIR = "./output/ui_test/" + TEST_NAME

os.makedirs(OUTPUT_DIR, mode=0o777, exist_ok=True)



# read cases
entries = os.listdir(CASES_DIR)
case_files = [e for e in entries if os.path.isfile(os.path.join(CASES_DIR, e))]
cases_collection = []

for f in case_files:
  csv = MyCSV(file="./cases/" + f, param_row=2, row_start=3, delimiter=",", encoding="shift_jis")
  cases_collection.append(csv.make_dict())
  shutil.copyfile("./cases/" + f, OUTPUT_DIR + "/" + f)



# execute test cases
for cases in cases_collection:
  for case in cases:
    test = MyTgiotUiTest(output=OUTPUT_DIR)
    test.exec_test(case)

print("done")
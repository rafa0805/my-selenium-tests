import csv

class CSV:

  # *************** Class Interface ***************
  def __init__(self, file, encoding="shift_jis", delimiter=",", lineterminator="\r\n", param_row="1", record_row="2"):
    csv_file = open(file, "r", encoding=encoding, errors="", newline="" )
    f = csv.reader(csv_file, delimiter=delimiter, doublequote=True, lineterminator=lineterminator, quotechar='"', skipinitialspace=True)
    # header = next(f)

    self.make_list(f)
    self.make_dictionary(param_row, record_row)

  def make_list(self, f):
    self.data_array = list()
    for row in f:
      self.data_array.append(row)

  def make_dictionary(self, param_row, record_row):
    params = self.data_array[int(param_row) - 1]
    records = self.data_array[int(record_row) - 1:]
    self.data_dict = list()


    for i in range(len(records) - 1):
      element_dict = dict()
      for p in range(len(params) - 1):
        element_dict[params[p]] = records[i][p]
      
      self.data_dict.append(element_dict)
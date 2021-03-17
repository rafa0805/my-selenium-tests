import csv

class CSV:

  # *************** Class Interface ***************
  def __init__(self, file, encoding="shift_jis", delimiter=",", lineterminator="\r\n", param_row=1, row_start=2, row_end=""):
    csv_file = open(file, "r", encoding=encoding, errors="", newline="")
    self.f = csv.reader(csv_file, delimiter=delimiter, doublequote=True, lineterminator=lineterminator, quotechar='"', skipinitialspace=True)
    self.param_row = param_row
    self.row_start = row_start
    self.row_end = row_end



  def make_list(self):
    # create and return row data as a "array"
    data_array = list()
    
    for row in self.f:
      data_array.append(row)
    
    return data_array



  def make_dict(self):
    # get data as array   
    data_array = self.make_list()

    # determine csv structure
    params = data_array[self.param_row - 1]
    records = data_array[self.row_start - 1:]
    
    # create and return data as a "dictionary"
    data_dict = list()

    for i in range(len(records)):
      element_dict = dict()

      for p in range(len(params)):
        element_dict[params[p]] = records[i][p]
      
      data_dict.append(element_dict)
      
    return data_dict
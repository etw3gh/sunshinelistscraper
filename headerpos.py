class HeaderPos:
  """
  determines the starting index of column headers
  data rows are formatted according to the headers
  having the index makes it easy to extract data from a row of text
  """
  def __init__(self):
    self.school = None
    self.last = None
    self.first = None
    self.title = None 
    self.salary = None
    self.taxable = None
    self.HEADER = 'Employer / Employeur'

  def get(self, txtfile):
    with open(txtfile) as tfile:
      lines = tfile.readlines()
      for line in lines:
        if self.HEADER in line:
          line = line.lstrip()
          self.school = line.index('Employer')
          self.last = line.index('Surname')
          self.first = line.index('Given')
          self.title = line.index('Position')
          self.salary = line.index('Salary')
          self.taxable = line.index('Taxable')
          break
    return self
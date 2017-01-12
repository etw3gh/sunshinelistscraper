import re

class Row:
  """
  structure for holding row data
  methods to convert a line of text into a Row object
  """
  def __init__(self, year):
    self.school = ''
    self.last = ''
    self.first = ''
    self.title = ''
    self.salary = ''
    self.taxable = ''
    self.year = year.split('_')[0]
    self.yint = int(self.year)

  def csv(self, line):
    linesplit = line.split(',')
    if len(linesplit) == 8:
      skipsector, ln, fn, sal, tax, s, t, skipyear = linesplit 
      self.clean_all(ln, fn, sal, tax, s, t)

  def html(self, line, headers=None):
    line = line.strip()	
    if '|' in line:
      linesplit = line.split('|')
    else:
      linesplit = self.split_on_multiple_spaces(line.replace('$', '  $'))
    lens = len(linesplit)

    S = headers.school    
    L = headers.last
    F = headers.first
    T = headers.title
    SA = headers.salary
    TX = headers.taxable
    END = len(line)
    if headers is not None:
      self.school = line[S:L].strip()
      self.last = line[L:F].strip()
      self.first = line[F:T].strip()
      self.title = line[T:SA].strip()
      self.salary = line[SA:TX].strip()
      self.taxable = line[TX:END].strip()       
    elif self.year == '1996' and lens == 7:
      skipuni, s, ln, fn, t, sal, tax = linesplit
      self.clean_all(ln, fn, sal, tax, s, t)
    elif lens == 6:
      s, ln, fn, t, sal, tax = linesplit
      self.clean_all(ln, fn, sal, tax, s, t)
    else:
      print (self.year + " bad line: " + line)

  def split_on_multiple_spaces(self, line):
      return re.split(" {2,}", line)

  def clean_all(self, ln, fn, sal, tax, s, t):
    self.school = self.clean(s)
    self.last = self.clean(ln)
    self.first = self.clean(fn)
    self.title = self.clean(t)
    self.salary = self.clean(sal)
    self.taxable = self.clean(t)

  def clean(self, item):
    c = item.rstrip('_').lstrip('_')
    c = c.replace('_', ' ').strip()
    return c

  def __str__(self):
    tostr = 'school: {}, name: {}, title: {}, salary: {}, taxable: {}, year: {}'
    name = "{} {}".format(self.first, self.last)
    output = tostr.format(self.school, name, self.title, self.salary, self.taxable, self.year)
    return output
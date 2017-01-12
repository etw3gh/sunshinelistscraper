#!/usr/bin/env python3
import os, re, sys
from row import Row
from csv import reader
from headerpos import HeaderPos

class Ripper:
  def __init__(self, urlsfile, ripsfolder):
    self.url_file = urlsfile 
    self.html = '.html'
    self.csv = '.csv'
    self.pdf = '.pdf'
    self.txt = '.txt'
    self.php = 'php'
    self.rips = ripsfolder
    # unfortunately the CSVs for 2015/2014 include all sectors so we grep for Universities only
    # the CSVs for these years are also formatted differently so 2 expressions are req'd
    self.csvGrep = " | grep -e '^\"Universities'  -e '^Universities' "
    
    if not os.path.exists(ripsfolder):
      os.makedirs(ripsfolder)


  def rip(self):
    with open(self.url_file) as u:
      lines = u.readlines()
      for line in lines:
        line = line.strip()
        urlline = line.split(' ')
        if len(urlline) != 2:
          continue
        year, url = urlline
        year = year.strip()
        yint = int(year.split('_')[0])

        url = url.strip()
        if line.endswith(self.html):
          htmlfile = self.wget(url, year, self.html)
          yint = int(year.split('_')[0])
          txtfile = self.html2text(htmlfile, yint)
          if yint >= 2009 and yint <= 2013:
            headers = HeaderPos()
            headers = headers.get(txtfile)
            self.process_html(txtfile, year, headers)         
          else:
            self.process_html(txtfile, year)
        elif self.php in line:
          txtfile = self.curl(url, year, "")
          pass # TODO
        elif line.endswith(self.pdf):
          pdffile = self.wget(url, year, self.pdf)
          txtfile = self.pdf2text(pdffile)
          self.process_pdf(txtfile, year)

        elif line.endswith(self.csv):
          txtfile = self.curl(url, year, self.csvGrep)
          self.process_csv(txtfile, year)
        else:
          sys.stderr.write('illegal url')
          continue

  def curl(self, url, year, pipedGrep):
    textfile = '{}/{}.txt'.format(self.rips, year)
    curl_cmd = 'curl "{}" {} > {}'.format(url, pipedGrep, textfile)    
    os.system(curl_cmd)
    return textfile    

  def wget(self, url, year, fileext):
    filename = '{}/{}{}'.format(self.rips, year,fileext)
    wget_command = 'wget -O {} {}'.format(filename, url)    
    os.system(wget_command)
    return filename

  def html2text(self, filename, year):
    """
    performs ht
        r = Rml2text conversion
    filters out lines not starting with '|'
    """
    textfile = filename.replace(self.html, self.txt)
    if year >= 2009 and year <= 2013:
      totext = "html2text -ascii -nometa -style pretty -width 300 {} > temp".format(filename)
      os.system(totext)

      # remove lines of text preceeding the header (starting with 'Employer')
      sed_cmd = "sed -n '/Employer/,$p' temp > {}".format(textfile)
      os.system(sed_cmd)
    else:    
      if year < 2009:
        totext_template = "html2text -ascii -nometa -style pretty -width 300 {} | grep '^|'  > {}" 
      else:
        # csv case (new)
        totext_template = "html2text -ascii -nometa -style pretty -width 300 {} > {}"

      totext_command = totext_template.format(filename, textfile)
      os.system(totext_command)

    return textfile

  def process_csv(self, csvfile, year):
    print('csv: ' + csvfile)
    with open(csvfile) as cfile:
      lines = cfile.readlines()
      for line in lines:
        if '$' not in line:
          continue

        # remove commas between double quotes
        purgecommas = re.sub(r'(?!(([^"]*"){2})*[^"]*$),', '', line)

        # remove double quotes 
        noquotes = purgecommas.replace('"', '')
        
        r = Row(year)
        r.csv(noquotes)
        
        print (str(r))

  def process_html(self, htmlfile, year, headers=None):
    with open(htmlfile) as hfile:
      lines = hfile.readlines()
      for line in lines:
        line = line.strip().lstrip('|').rstrip('|').replace('_', ' ')

        if '$' not in line:
          continue
        print (line)
        #r = Row(year)
        #r.html(line, headers)
        #print(str(r))


if __name__== "__main__":
  #r = Ripper('urls_html.txt', 'rips')
  #r.rip()
  r = Ripper('urls_php.txt', 'rips')
  r.rip()
  r = Ripper('urls_csv.txt', 'rips')
  r.rip()    

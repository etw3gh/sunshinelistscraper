# Sunshine List University Data (Ontario)

This is a scraper and collector of semi open data provided by the Ontario Finance Ministry.

Once data is standardized into Row objects (see row.py), each row is pushed to a sqlite3 database.

A [microservice](https://github.com/openciti/sunshinemicroservice) will use the data to serve web pages and a twitter bot

## data sources

Each year comes in a different format

There is a combination of html pages, php sites and csv downloads with annoying differences everywhere.

see urls_csv.txt, urls_html.txt & urls_php.txt 

## dependencies

sudo apt install html2text

## usage

python3 ripper.py 

this will invoke the following:

if __name__== "__main__":
  r = Ripper('urls_html.txt', 'rips')
  r.rip()
  r = Ripper('urls_php.txt', 'rips')
  r.rip()
  r = Ripper('urls_csv.txt', 'rips')
  r.rip()  

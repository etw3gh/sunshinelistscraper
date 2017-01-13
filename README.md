# Sunshine List University Data (Ontario)

This is a scraper and collector of semi open data provided by the Ontario Finance Ministry.

Once data is standardized into Row objects (see row.py), each row is pushed to a sqlite3 database.

A [microservice](https://github.com/openciti/sunshinemicroservice) to serve web data

An interactive [twitter bot](https://github.com/openciti/sunshinelistbot)

[@myprofmakes](https://twitter.com/MyProfMakes) will serve the data over twitter

## data sources

Each year comes in a different format

There is a combination of html pages, php sites and csv downloads with annoying differences everywhere.

## dependencies

sudo apt install html2text

## usage

python3 ripper.py

right now the main method of ripper.py (line 145)

you need a block of code like this for each urls file

```
r = Ripper(urlslist, ripsfolder, force-download, serviceurl)

r.rip()
```

###urlslist

a text file with a list of urls and years:

>urls_csv.txt
>urls_html.txt
>urls_php.txt

for years covered in a single url:

2020 https://on.gov/2020_salaries.html

for years with multiple urls:

2030_0 https://on.gov/2030_salaries_a.html
2030_1 https://on.gov/2030_salaries_b.html


### ripsfolder

full path for where you want the downloaded data and process text files to reside.

it will be created for you

### force-download

will download data from the urls even if files are already present

### serviceurl

url for a web service that will store the data

its must be similar to [this microservice](https://github.com/openciti/sunshinemicroservice)

## warning

data from 1996 to 2015 took over 15 hours to download, process and upload

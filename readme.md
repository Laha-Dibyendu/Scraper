# Introduction

### **json-links** - It contains all the json files wit college links, courses links and exam links.

### **Scraped data** - This is the folder where you store all the output files.

### **Scraper** - This folder contains the actual code inside spider folder in it.

- The `college_spider.py` file contains the code to scrape details about the colleges.

- The `course_spider.py` file contains scrapy code to scrape courses links.

- The `exam_spider.py` contains the code to scrape the data from the exam links.
# Steps to run this project

* First you have to create a virtual environment for that you can use either 

`pip` or `pipenv`
 If you are using pipenv write 

        pipenv shell

to create a virual env.

* Next you have to install all the requirements, for that you just have to run 

        pipenv install requirements.txt

     it will install all the packcages needed to run this project.

* Now go inside the folder **Scraper** in the terminal.

* Run 

        scrapy crawl {name of the spider} -O scraped_data/{name of the csv}.csv

     withoout the curly brackets.

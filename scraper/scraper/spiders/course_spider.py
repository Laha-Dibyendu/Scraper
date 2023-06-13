from pathlib import Path
import json
import scrapy


######################################### Scraper for scraping Course details #################

class CoursepSpider(scrapy.Spider):
    name = "coursep"
    allowed_domains = ['engineering.careers360.com']
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}

    path = "json-links/"
    with open(path+'IN-course-certification.json') as f:
        links = json.load(f)

    
    #start_requests() method is used to generate the initial requests that Scrapy will make to begin scraping a website.
    def start_requests(self):
        start_urls = self.links
        for urls in start_urls:
            for key in urls:
                self.ko = key
                yield scrapy.Request(url=urls[key], callback=self.parse) #redirecting to parse() method

    #the parse() method is used to extract data from a website's response after a request has been made. 
    # response - response refers to the object that represents the HTTP response returned from a website after a request has been made. It contains the raw HTML content of the page, as well as other metadata such as the URL, headers, and status code.
    # return?? - In this case it wil return dictionary object 
    def parse(self, response):
        tutsitem={}
        tutsitem["course_name"]=response.xpath('/html/body/div[1]/div[2]/section[1]/div/div/div[1]/div[2]/h1/text()').get()
        tutsitem["fees"]=response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[1]/div[1]/div/p/text()")[1].get()
        tutsitem["duration"] = "".join(response.css("#course_detail > p > span:nth-child(2)::text").getall())
        tutsitem["detail"]="".join(response.css("#course_detail > div > p::text").getall())
        tutsitem["offering"]=" ".join(response.css("#programme_offering > div > ul > li::text").getall())
        tutsitem["eligibility"]="".join(response.css("#eligiblity > div > div > p::text").getall())
        tutsitem["admission"]=response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[5]/div/p/text()").getall()
        tutsitem["semester_1"]=response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[6]/div/div[2]/div[1]/div/div/div/ul/li/text()").getall()
        tutsitem["semester_2"]=response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[6]/div/div[2]/div[2]/div/div/div/ul/li/text()").getall()
        tutsitem["semester_3"]=response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[6]/div/div[2]/div[3]/div/div/div/ul/li/text()").getall()
        tutsitem["semester_4"]=response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[6]/div/div[2]/div[4]/div/div/div/ul/li/text()").getall()
        tutsitem["semester_5"]=response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[6]/div/div[2]/div[5]/div/div/div/ul/li/text()").getall()
        tutsitem["semester_6"]=response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[6]/div/div[2]/div[6]/div/div/div/ul/li/text()").getall()
        tutsitem["semester_7"]=response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[6]/div/div[2]/div[7]/div/div/div/ul/li/text()").getall()
        tutsitem["semester_8"]=response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[6]/div/div[2]/div[8]/div/div/div/ul/li/text()").getall()
        tutsitem["evaluation"]=response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[6]/div/div[3]/p/text()").getall()
        jk=response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[7]/div/div/div").getall()
        tutsitem["faq"]=[]
        for i in range(len(jk)):
            tutsitem["faq"].append(str(response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[7]/div/div/div[{}]/div[1]/text()[3]'.format(i+1)).get()) + " : " + str(response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[7]/div/div/div[{}]/div[2]/div/p/text()'.format(i+1)).get()))
        yield tutsitem
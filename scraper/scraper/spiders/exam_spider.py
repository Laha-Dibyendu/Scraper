import scrapy

import json

################################## Scraper for scraping Exam details #########################################3

class ExamsSpider(scrapy.Spider):
    name = "exams"
    allowed_domains = ['engineering.careers360.com']
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    
    path = "json-links/"
    with open(path+'exam_link.json') as f:
        links = json.load(f)

    
    #start_requests() method is used to generate the initial requests that Scrapy will make to begin scraping a website.
    def start_requests(self):
        start_urls = self.links
        for urls in start_urls:
            for key in urls:
                yield scrapy.Request(url=urls[key], callback=self.parse) #redirecting to parse() method


    #the parse() method is used to extract data from a website's response after a request has been made. 
    # response - response refers to the object that represents the HTTP response returned from a website after a request has been made. It contains the raw HTML content of the page, as well as other metadata such as the URL, headers, and status code.
    # return?? - In this case it wil return dictionary object 
    def parse(self, response):
        tutsitem={
            "exam_name":"NA",
            "about":"NA",
            "full_exam_name":"NA",
            "short_exam_name":"NA",
            "conducting_body":"NA",
            "freq_of_conduct":"NA",
            "exam_level":"NA",
            "languages":"NA",
            "mode_of_application":"NA",
            "application_fee":"NA",
            "mode_of_exam":"NA",
            "mode_of_counselling":"NA",
            "exam_duration":"NA",
            "number_of_seats":"NA",
            "education":"NA",
            "age":"NA",
            "website_link":"NA",
            "exam_pattern":"NA"

        }

        lis=response.css("#highlights > div > table > tbody > tr > td:nth-child(1)::text").getall()
        for i in lis:
            c= lis.index(i)+1
            if i == "Full Exam Name":
                tutsitem["full_exam_name"]=response.css("#highlights > div > table > tbody > tr:nth-child({}) > td:nth-child(2)::text".format(c)).get()
            elif i=="Short Exam Name":
                tutsitem["short_exam_name"] =response.css("#highlights > div > table > tbody > tr:nth-child({}) > td:nth-child(2)::text".format(c)).get()
            elif i=="Conducting Body":
                tutsitem["conducting_body"]=response.css("#highlights > div > table > tbody > tr:nth-child({}) > td:nth-child(2)::text".format(c)).get()
            elif i=="Frequency of Conduct":
                tutsitem["freq_of_conduct"] =response.css("#highlights > div > table > tbody > tr:nth-child({}) > td:nth-child(2)::text".format(c)).get()
            elif i=="Exam Level":
                tutsitem["exam_level"] =response.css("#highlights > div > table > tbody > tr:nth-child({}) > td:nth-child(2)::text".format(c)).get()
            elif i=="Languages":
                tutsitem["languages"] =response.css("#highlights > div > table > tbody > tr:nth-child({}) > td:nth-child(2)::text".format(c)).get()
            elif i=="Mode of Application":
                tutsitem["mode_of_application"] =response.css("#highlights > div > table > tbody > tr:nth-child({}) > td:nth-child(2)::text".format(c)).get()
            elif i=="Application Fee (General)":
                tutsitem["application_fee"] = (response.css("#highlights > div > table > tbody > tr:nth-child({}) > td:nth-child(2)::text".format(c)).get()).split("[")[0]
            elif i=="Mode of Exam":
                tutsitem["mode_of_exam"] =response.css("#highlights > div > table > tbody > tr:nth-child({}) > td:nth-child(2)::text".format(c)).get()
            elif i=="Mode of Counselling":
                tutsitem["mode_of_counselling"] = response.css("#highlights > div > table > tbody > tr:nth-child({}) > td:nth-child(2)::text".format(c)).get()
            elif i=="Exam Duration":
                tutsitem["exam_duration"] =response.css("#highlights > div > table > tbody > tr:nth-child({}) > td:nth-child(2)::text".format(c)).get()
            elif i=="Number of Seats":
                tutsitem["number_of_seats"] =response.css("#highlights > div > table > tbody > tr:nth-child({}) > td:nth-child(2)::text".format(c)).get()


        tutsitem["exam_name"]=response.css("body > div.mainContainer.rightSidebar > div.container > ul > li:nth-child(3)::text").get()
        tutsitem["about"] =response.xpath("/html/body/div[4]/section/div/div/div[1]/div[2]/div[2]/div[1]/div/div/p[1]/text()").get() if response.xpath("/html/body/div[4]/section/div/div/div[1]/div[2]/div[2]/div[1]/div/div/p[1]/text()").getall() else "NA"
        tutsitem["education"]= response.xpath("/html/body/div[4]/section/div/div/div[1]/div[8]/div[2]/div[1]/div/div/p[3]/text()").get() if "Education" in response.xpath("/html/body/div[4]/section/div/div/div[1]/div[8]/div[2]/div[1]/div/div/p[3]/strong/text()").getall() else "NA"
        tutsitem["age"]= response.xpath("/html/body/div[4]/section/div/div/div[1]/div[8]/div[2]/div[1]/div/div/p[4]/text()").get() if "Age" in response.xpath("/html/body/div[4]/section/div/div/div[1]/div[8]/div[2]/div[1]/div/div/p[4]/strong/text()").getall() else "NA"
        tutsitem["exam_pattern"]= response.xpath("/html/body/div[4]/section/div/div/div[1]/div[13]/div[2]/div[1]/div/div/p/text()").getall() if response.xpath("/html/body/div[4]/section/div/div/div[1]/div[13]/div[2]/div[1]/div/div/p/text()").get() else "NA"
        tutsitem["website_link"]= response.css("body > div.mainContainer.rightSidebar > section > div > div > div.contentPart > div:nth-child(22) > div.boxesLayout.generalInformation > div > div > div > div.headingSecound > a::attr(href)").get() if response.css("body > div.mainContainer.rightSidebar > section > div > div > div.contentPart > div:nth-child(22) > div.boxesLayout.generalInformation > div > div > div > div.headingSecound > a").get() else "NA"
        yield tutsitem
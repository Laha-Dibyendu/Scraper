import scrapy
import json
import os

####################################### Scraper for scraping college details ################################
class CollegesSpider(scrapy.Spider):
    name = "colleges"
    allowed_domains = ['engineering.careers360.com']
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}

    path = "json-links/"
    with open(path+"ts-engg-colleges.json") as f:
        links = json.load(f)


    #start_requests() method is used to generate the initial requests that Scrapy will make to begin scraping a website.
    def start_requests(self): 
        
        start_urls = self.links
        for urls in start_urls:
            for key in urls:
                yield scrapy.Request(url=urls[key].split("?")[0], callback=self.parse) #redirecting to parse() method


    #the parse() method is used to extract data from a website's response after a request has been made. 
    # response - response refers to the object that represents the HTTP response returned from a website after a request has been made. It contains the raw HTML content of the page, as well as other metadata such as the URL, headers, and status code.
    # return?? - In this case it wil return dictionary object
    def parse(self, response):
        tutsitem={
            'college_name':"NA",
            "about":"NA",
            "address":"NA",
            'affiliated':"NA",
            'state':"NA",
            'college_type':"NA",
            'established':"NA",
            'exam':"NA",
            'courses':"NA",
            'accreditations':"NA",
            'approvals':"NA",
            'gender':"NA",
            'student_count':"NA",
            'faculty_count':"NA",
            'gender_percentage':"NA",
            'campus_size':"NA",
            "website_link":response.url

        }

        lis=response.css('div#highlight > div.highlight > div.table-responsive > table.table > tbody > tr > td:first-child::text').getall()
        
        for i in lis:
            c= lis.index(i)+1
            if i == "Established":
                tutsitem['established'] = response.css('div#highlight > div.highlight > div.table-responsive > table.table > tbody > tr:nth-child({}) > td:last-child::text'.format(c)).get()
            elif i == "Exam":
                tutsitem['exam'] = response.css('div#highlight > div.highlight > div.table-responsive > table.table > tbody > tr:nth-child({}) > td:last-child > span > a::text'.format(c)).getall()
            elif i == "Courses":
                tutsitem['courses'] = response.css('div#highlight > div.highlight > div.table-responsive > table.table > tbody > tr:nth-child({}) > td:last-child > a::text'.format(c)).getall()
            elif i == "Accreditations":
                tutsitem['accreditations'] = response.css('div#highlight > div.highlight > div.table-responsive > table.table > tbody > tr:nth-child({}) > td:last-child > span::text'.format(c)).get()
            elif i == "Approvals":
                tutsitem['approvals'] = response.css('div#highlight > div.highlight > div.table-responsive > table.table > tbody > tr:nth-child({}) > td:last-child > span::text'.format(c)).get()
            elif i == "Gender":
                tutsitem['gender'] = response.css('div#highlight > div.highlight > div.table-responsive > table.table > tbody > tr:nth-child({}) > td:last-child::text'.format(c)).get()
            elif i == "Student count":
                tutsitem['student_count'] = response.css('div#highlight > div.highlight > div.table-responsive > table.table > tbody > tr:nth-child({}) > td:last-child::text'.format(c)).get()
            elif i == "Faculty count":
                tutsitem['faculty_count'] = response.css('div#highlight > div.highlight > div.table-responsive > table.table > tbody > tr:nth-child({}) > td:last-child::text'.format(c)).get()
            elif i == "Gender percentage":
                tutsitem['gender_percentage'] = response.css('div#highlight > div.highlight > div.table-responsive > table.table > tbody > tr:nth-child({}) > td:last-child::text'.format(c)).get()
            elif i == "Campus size":
                tutsitem['campus_size'] = response.css('div#highlight > div.highlight > div.table-responsive > table.table > tbody > tr:nth-child({}) > td:last-child::text'.format(c)).getall()

        
        tutsitem['college_name'] = response.css('nav.article_breadcrumb > ol.breadcrumb > li.active::text').get()
        tutsitem['about']= response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[1]/div/div[1]/div/p[1]/text()").getall() if response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[1]/div/div[1]/div/p[1]/text()").getall() else "NA"
        tutsitem['affiliated'] = response.css('div.bannerTags:last-child > span:last-child > a::text').get() if response.css('div.bannerTags:last-child > span:last-child > a::text').get()!=None else "NA"
        tutsitem['state'] = response.css('div.bannerTags > span > a:last-child::text').get() if response.css('div.bannerTags > span > a:last-child::text').get() else "NA"
        tutsitem['college_type'] = response.css('div.bannerTags:last-child > span::text').get() if response.css('div.bannerTags:last-child > span::text').get() else "NA"
        tutsitem['address']= response.css('#contact > div > div > div.contct.col-sm-5::text').get()
        yield tutsitem


#################################################### Scraper for scraping courses ########################################

class CourseSpider(scrapy.Spider):
    name = "courses"
    allowed_domains = ['engineering.careers360.com']
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    
    
    path = "json-links/"
    with open(path+"ts-engg-colleges.json") as f:
        links = json.load(f)


    #start_requests() method is used to generate the initial requests that Scrapy will make to begin scraping a website.
    def start_requests(self): 
        start_urls = self.links
        for urls in start_urls:
            for key in urls:
                yield scrapy.Request(url=urls[key].split("?")[0]+"/courses", callback=self.parse) #redirecting to parse() method


    #the parse() method is used to extract data from a website's response after a request has been made. 
    # response - response refers to the object that represents the HTTP response returned from a website after a request has been made. It contains the raw HTML content of the page, as well as other metadata such as the URL, headers, and status code.
    # return?? - In this case it wil return dictionary object 
    def parse(self, response):
        tutsitem={
            "website_link":response.url}
        for course in response.css('div.course_list'):
            for c in course.css('div.detail'):
                tutsitem['college_name'] = response.css('nav.article_breadcrumb > ol.breadcrumb > li:nth-child(4) > a::text').get()
                tutsitem['course_name']= c.css('h4 > a::text').get()
                tutsitem['course_link'] = c.css('h4 > a::attr(href)').get()
                tutsitem['course_duration']= c.css('div.course_detail > div:nth-child(2) > span::text').get() if c.css('div.course_detail > div:nth-child(2) > span::text').get()!=(None or " ") else "NA"
                tutsitem['course_type']= c.css('div.course_detail > div:nth-child(3) span::text')[1].getall() if c.css('div.course_detail > div:nth-child(3) span::text')[1].getall()!=(None or " ") else "NA"
                tutsitem['fees']= c.css('div.course_detail > div:nth-child(4) > span::text').getall() if c.css('div.course_detail > div:nth-child(4)::text').get()== "Total Fees:" else "NA"
                tutsitem['seats']= c.css('div.course_detail > div:last-child > span::text').get() if c.css('div.course_detail > div:last-child::text').get()== "Seats: " else "NA"
                yield tutsitem

##################################################### Scraper for scraping cutoff details #########################################

class CutoffSpider(scrapy.Spider):
    name = "cutoff"
    allowed_domains = ['engineering.careers360.com']
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    
    path = "json-links/"
    with open(path+"ts-engg-colleges.json") as f:
        links = json.load(f)

    #start_requests() method is used to generate the initial requests that Scrapy will make to begin scraping a website.
    def start_requests(self): 
        start_urls = self.links
        for urls in start_urls:
            for key in urls:
                yield scrapy.Request(url=urls[key].split("?")[0]+"/cut-off", callback=self.parse) #redirecting to parse() method


    #the parse() method is used to extract data from a website's response after a request has been made. 
    # response - response refers to the object that represents the HTTP response returned from a website after a request has been made. It contains the raw HTML content of the page, as well as other metadata such as the URL, headers, and status code.
    # return?? - In this case it wil return dictionary object 
    def parse(self, response):
        tutsitem={
            "website_link":response.url}
        tutsitem['college_name'] = response.css('nav.article_breadcrumb > ol.breadcrumb > li:nth-child(4) > a::text').get()
        l=int(str(response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[2]/div/div[1]/strong/text()[2]').getall()[0]))
        
        sm_9_div=3 # div class named as col-sm-9
        sm_7_div=1 # div class named as col-sm-7
        tr=1 # tr tag  inside the table of div.col-sm-7
        td=2 ## tr tag  inside the table of div.col-sm-7
        
        while sm_9_div <=l+3:

            tutsitem['course_name']= response.css('#root > div.college_main_container > section:nth-child(4) > div > div.row > div.left_column.col-sm-9 > div:nth-child(2) > div > div:nth-child({}) > div.col-sm-5 > a::text'.format(sm_9_div)).get()
            tutsitem["2021 closing rank"]= response.css('#root > div.college_main_container > section:nth-child(4) > div > div.row > div.left_column.col-sm-9 > div:nth-child(2) > div > div:nth-child({}) > div.year.col-sm-7 > div:nth-child({}) > div > strong::text'.format(sm_9_div,sm_7_div)).get() if response.css('#root > div.college_main_container > section:nth-child(4) > div > div.row > div.left_column.col-sm-9 > div:nth-child(2) > div > div:nth-child({}) > div.year.col-sm-7 > div:nth-child({}) > strong::text'.format(sm_9_div,sm_7_div)).get()=="2021" else "NA"
            tutsitem["2020 closing rank"]= response.css('#root > div.college_main_container > section:nth-child(4) > div > div.row > div.left_column.col-sm-9 > div:nth-child(2) > div > div:nth-child({}) > div.year.col-sm-7 > div:nth-child({}) > div > strong::text'.format(sm_9_div,sm_7_div+1)).get() if response.css('#root > div.college_main_container > section:nth-child(4) > div > div.row > div.left_column.col-sm-9 > div:nth-child(2) > div > div:nth-child({}) > div.year.col-sm-7 > div:nth-child({}) > strong::text'.format(sm_9_div,sm_7_div+1)).get()=="2020" else "NA"
            tutsitem["Category"]= response.css('#root > div.college_main_container > section:nth-child(4) > div > div.row > div.left_column.col-sm-9 > div.cutt_off > div.table-responsive-sm.table_block > table > tbody > tr:nth-child({}) > td:nth-child({})::text'.format(tr,td)).get() if response.css('#root > div.college_main_container > section:nth-child(4) > div > div.row > div.left_column.col-sm-9 > div.cutt_off > div.table-responsive-sm.table_block > table > tbody > tr:nth-child({}) > td:nth-child({})::text'.format(tr,td)).get() else "NA"
            tutsitem["opening_home_state_rank"]= response.css('#root > div.college_main_container > section:nth-child(4) > div > div.row > div.left_column.col-sm-9 > div.cutt_off > div.table-responsive-sm.table_block > table > tbody > tr:nth-child({}) > td:nth-child({})::text'.format(tr,td+1)).get() if response.css('#root > div.college_main_container > section:nth-child(4) > div > div.row > div.left_column.col-sm-9 > div.cutt_off > div.table-responsive-sm.table_block > table > tbody > tr:nth-child({}) > td:nth-child({})::text'.format(tr,td+1)).get() else "NA"
            tutsitem["closing_home_state_rank"]= response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[4]/div[1]/table/tbody/tr[{}]/td[{}]/text()'.format(tr,td+2))[1].get() if response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[4]/div[1]/table/tbody/tr[{}]/td[{}]/text()'.format(tr,td+2))[1].get() else "NA"
            sm_9_div+=1
            tr+=1
            yield tutsitem


##################################################### Scraper for scraping facility details ###################################

class FacilitySpider(scrapy.Spider):
    name = "facility"
    allowed_domains = ['engineering.careers360.com']
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}

    
    path = "json-links/"
    with open(path+"ts-engg-colleges.json") as f:
        links = json.load(f)

    #start_requests() method is used to generate the initial requests that Scrapy will make to begin scraping a website.
    def start_requests(self): 
        start_urls =  self.links
        for urls in start_urls:
            for key in urls:
                yield scrapy.Request(url=urls[key].split("?")[0]+"/facilities", callback=self.parse) #redirecting to parse() method

    #the parse() method is used to extract data from a website's response after a request has been made. 
    # response - response refers to the object that represents the HTTP response returned from a website after a request has been made. It contains the raw HTML content of the page, as well as other metadata such as the URL, headers, and status code.
    # return?? - In this case it wil return dictionary object 
    def parse(self, response):
        tutsitem={
            "website_link":response.url}
        tutsitem['college_name'] = response.css('nav.article_breadcrumb > ol.breadcrumb > li:nth-child(4) > a::text').get()
        o=1
        li=response.css('#root > div.college_main_container > div.container > div.row > div.left_column.col-sm-9 > div:nth-child(1) > div > ul > li').getall()
        while o<=len(li):
            tutsitem['facility_name']= response.css('#root > div.college_main_container > div.container > div.row > div.left_column.col-sm-9 > div:nth-child(1) > div > ul > li:nth-child({}) > div.facilities_wrap > span.facilities_name::text'.format(o)).get()
            tutsitem['description']= response.xpath('/html/body/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div/ul/li[{}]/div[2]/p/text()'.format(o)).get()
            o+=1
            yield tutsitem


# class CourselinkSpider(scrapy.Spider):
#     name = "courseslink"
#     allowed_domains = ['engineering.careers360.com']
#     headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    
    
#     path = "json-links/"
#     with open(path+"ts-engg-colleges.json") as f:
#         links = json.load(f)


#     #start_requests() method is used to generate the initial requests that Scrapy will make to begin scraping a website.
#     def start_requests(self): 
#         start_urls = self.links
#         for urls in start_urls:
#             for key in urls:
#                 yield scrapy.Request(url=urls[key].split("?")[0]+"/courses", callback=self.parse) #redirecting to parse() method


#     #the parse() method is used to extract data from a website's response after a request has been made. 
#     # response - response refers to the object that represents the HTTP response returned from a website after a request has been made. It contains the raw HTML content of the page, as well as other metadata such as the URL, headers, and status code.
#     # return?? - In this case it wil return dictionary object 
#     def parse(self, response):
#         tutsitem={
#             "website_link":response.url,
#             "course_name":"NA",
#             "offered_by":"NA",
#             "course_link":"NA",
#             # "course_overview":"NA",
#             # "course_details":'NA',
#             # "eligibility_criteria":"NA",
#             # "admission_detail":"NA"
#             }
        
#         # for course in response.css('div.course_list'):
#         #     for c in course.css('div.detail'):
#         for j in range(1,int(response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[2]/div[2]/div[1]/text()[2]').get())+1):
#             tutsitem['course_name']= response.css('#root > div.undefined.college_main_container > section.courses_fees > div > div.row > div.left_column.col-sm-9 > div.course_list > div:nth-child({}) > div.detail > h4 > a::text'.format(j+1)).get()
#             tutsitem['offered_by'] = response.css('#root > div.undefined.college_main_container > section.banner > div.container > nav > ol > li:nth-child(4) > a::text').get()
#             tutsitem['course_link']= response.css('#root > div.undefined.college_main_container > section.courses_fees > div > div.row > div.left_column.col-sm-9 > div.course_list > div:nth-child({}) > div.detail > h4 > a::attr(href)'.format(j+1)).get()
#             yield tutsitem



class Course_ovSpider(scrapy.Spider):
    name = "courseov"
    allowed_domains = ['engineering.careers360.com']
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    
    
    path = "scraped_data/"
    with open(path+"ts_cor.json") as f:
        links = json.load(f)


    #start_requests() method is used to generate the initial requests that Scrapy will make to begin scraping a website.
    def start_requests(self): 
        start_urls = self.links
        for urls in start_urls:
            #for key in urls:
            if urls['course_link']:
                yield scrapy.Request(url="https://www.careers360.com"+urls['course_link'], callback=self.parse) #redirecting to parse() method


    #the parse() method is used to extract data from a website's response after a request has been made. 
    # response - response refers to the object that represents the HTTP response returned from a website after a request has been made. It contains the raw HTML content of the page, as well as other metadata such as the URL, headers, and status code.
    # return?? - In this case it wil return dictionary object 
    def parse(self, response):
        tutsitem={
            "website_link":response.url,
            "course_name":"NA",
            "offered_by":"NA",
            "fees":"NA",
            #"course_link":"NA",
            "course_overview":"NA",
            "course_details":'NA',
            "eligibility_criteria":"NA",
            "admission_detail":"NA"
            }
        
        # for course in response.css('div.course_list'):
        #     for c in course.css('div.detail'):
        #for j in range(1,int(response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[2]/div[2]/div[1]/text()[2]').get())+1):
        tutsitem['course_name']= response.xpath('/html/body/div[1]/div[2]/section[1]/div/nav/ol/li[4]/text()').get()
        tutsitem['offered_by'] = response.css('#root > div.college_main_container.course_detail_page > section.banner.course_detail_banner > div > div > div.banner_detail.banner_detail_certificate > div.college_detail > div.bannerTags > span:nth-child(1) > a::text').get()
        tutsitem["fees"]= response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[1]/div/table/tbody/tr/td[1]/div/div[2]/div[2]/span/text()').get() if response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[1]/div/table/tbody/tr/td[1]/div/div[2]/div[1]/text()').get() == ' Total Fees ' else "NA"
        tutsitem['course_overview']= response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[3]/div/div/p/text()').get() #if response.xpath("/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[3]/h2/text()") == "Course Overview" else "NA"
        tutsitem['course_details']= response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[4]/div/p/text()').get() #if response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[4]/h2/text()').get() == "Course Details" else "NA"
        tutsitem['eligibility_criteria']= response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[5]/div/div/p/text()').get() #if response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[5]/h2/text()').get() == "Eligibility Criteria"  else "NA"
        tutsitem['admission_detail'] = response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[6]/div/p/text()').get() #if response.xpath('/html/body/div[1]/div[2]/section[2]/div/div[1]/div[1]/div[6]/h2').get() == ' Admission Details' else "NA"
        yield tutsitem
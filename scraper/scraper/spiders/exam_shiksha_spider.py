from pathlib import Path
import json
import scrapy


######################################### Scraper for scraping Course details #################

class examp_shikshaSpider(scrapy.Spider):
    name = "exam_sh"
    allowed_domains = ['shiksha.com']
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}

    path = "json-links/"
    with open(path+'shiksha.json') as f:
        links = json.load(f)

    
    #start_requests() method is used to generate the initial requests that Scrapy will make to begin scraping a website.
    def start_requests(self):
        start_urls = self.links
        
        for urls in start_urls:
            for key in urls:
                yield scrapy.Request(url="https://www.shiksha.com"+urls[key], callback=self.parse) #redirecting to parse() method
                #yield scrapy.Request(url=urls+"-pattern", callback=self.parse2)

    #the parse() method is used to extract data from a website's response after a request has been made. 
    # response - response refers to the object that represents the HTTP response returned from a website after a request has been made. It contains the raw HTML content of the page, as well as other metadata such as the URL, headers, and status code.
    # return?? - In this case it wil return dictionary object 
    def parse(self, response):
        tutsitem={
            "exam_name":"NA",
            "exam_link":"NA",

            "overview":"NA",
            "upcoming_date":"NA",
            "exam_name":"NA",
            "conducting_body":"NA",
            "exam_level":"NA",
            "exam_frequency":"NA",
            "mode_of_exam":"NA",
            
            "exam_pattern":"NA",
            "eligibility_criteria":"NA",
            
            "courses_offered":"NA",
            "application_fees":"NA",
            "exam_duration":"NA",
            "total_marks":"NA",
            "total_questions":"NA",
            "marking_scheme":"NA",
            "medium_of_exam":"NA",
            "colleges_accepting_exam_score":"NA",
            "official_website":"NA",
            "contact_details":"NA",
            "latest_updates":"NA"

        }
        tutsitem["exam_name"]=response.css("#breadCrumb > span:nth-child(7) > span::text").get()
        tutsitem["exam_link"]= response.url
        tutsitem["overview"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[4]/div/p[6]/text()").getall()
        tutsitem["upcoming_date"]= response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[5]/div/table/tbody/tr[2]/td[1]/p/text()").getall()+response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[5]/div/table/tbody/tr[2]/td[2]/p/text()").getall() if response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[5]/div/table/tbody/tr[1]/th[2]/text()").get() == "Upcoming Exam Dates" else "NA"
        tutsitem["latest_updates"]= response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[4]/div/p/strong/text()").get()#+response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[4]/div/p/text()").getall()

        tr_count = len(response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr").getall())+1 
        if tr_count > 1:

            for tr in range(1, tr_count):
                
                if response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).get() == "Exam Name":
                    tutsitem["exam_name"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).get() == "Conducting Body":
                    tutsitem["conducting_body"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()

                elif response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).get() == "Exam Level":
                    tutsitem["exam_level"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).get() == "Exam Frequency":
                    tutsitem["exam_frequency"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).get() == "Mode of Exam":
                    tutsitem["mode_of_exam"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).get() == "Courses offered through the Entrance Exam":
                    tutsitem["courses_offered"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif "Fees" in "".join(response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).getall()) :
                    
                    tutsitem["application_fees"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).get() == "Exam Duration":
                    tutsitem["exam_duration"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif "Total Marks" in "".join(response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).getall() ):
                    tutsitem["total_marks"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif "Total Questions" in "".join(response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).getall() ):
                    tutsitem["total_questions"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).get() == "Marking Scheme":
                    tutsitem["marking_scheme"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif "Medium of Exam" in "".join(response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).getall() ):
                    tutsitem["medium_of_exam"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).get() == "Colleges Accepting Exam Score":
                    tutsitem["colleges_accepting_exam_score"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif "Website" in "".join(response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).getall() ):
                    tutsitem["official_website"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
                elif response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(tr)).get() == "Contact Details":
                    tutsitem["contact_details"] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[6]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(tr)).getall()
                
        
        yield tutsitem

    def parse2(self, response):
        tutsitem=response.meta["data"]
        
        D={}
        for item in range(2,len(response.css("#wikkiContents_pattern_0_0 > div > table:nth-child(12) > tbody > tr").getall())+1):
            D[response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[4]/div/table[1]/tbody/tr[{}]/td[1]/p/text()".format(item)).get()] = response.xpath("/html/body/div[3]/main/div/section/div/div[3]/div[1]/section[1]/div/div/div[4]/div/table[1]/tbody/tr[{}]/td[2]/p/text()".format(item)).getall()

        tutsitem.update(D)
        print(tutsitem)
        return tutsitem
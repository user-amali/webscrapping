# This program crawls subcategory (and its subcategories) from the domain http://dmoztools.net. 
# The dmoztools.net is the directory of webpages for different categories.
# At this stage, it will crawl dmoztools.net/computer/freeware and its subcategories for (web)sites 
# listed on each of the pages. This program can run until it has crawled all the pages unless 
# the spider is stopped by Ctrl+C. As this can cause too much traffic, further versions of this program
# will have extensions/spider settings to stop the spider when it reaches a certain limit.

import scrapy
import re

class cataloguespider(scrapy.Spider):
    name = "cataloguespider"
    start_urls = [
        'http://dmoztools.net/Computers/Software/Freeware'
    ]
    

    def parse(self, response): 
        site = response.css('div.site-item').get()
        if site is not None:
            cat_list = []
            for categoryname in response.css('a.breadcrumb::text').getall():
                cat_list.append(categoryname)
                cat_list.append('/')
            category = ''.join(cat_list)
            re.sub(r"^\s+|\s+$", "", category)
            
            for site in response.css('div.site-item'):
                yield{
                    'Category': category,
                    'WebsiteName': site.css('div.title-and-desc div.site-title::text').get(),
                    'WebsiteURL': site.css('div.title-and-desc a::attr(href)').get(),
                    'Description': site.css('div.title-and-desc div.site-descr::text').get(),
                } 
        anchors = response.css('div.cat-item a')
        yield from response.follow_all(anchors, callback=self.parse)
    

           
                
                

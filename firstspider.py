# This program crawls subcategory (and its subcategories) from the domain http://dmoztools.net. 
# The dmoztools.net is the directory of webpages for different categories.
# At this stage, it will crawl dmoztools.net/computer/software/freeware and its subcategories for (web)sites 
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
        # reads website/ site details from the response page
        site = response.css('div.site-item').get()
        if site is not None:
            cat_list = []
            # Get the page title from breadcrumbs. 
            # The previous page titles need to be appended to get the current full title.
            # for categoryname in response.css('a.breadcrumb::text').getall():
            #    cat_list.append(categoryname)
            #    cat_list.append('/')
            # Append the last item to the title
            #category = ''.join(cat_list)
         
            
            # Get category from the title for the webpage
            # Also, get websitename, url, and description for the website links
            # listed on the response webpage
            for site in response.css('div.site-item'):
                # get categorytitle and remove leading '/desc/'
                categorytitle = response.css('div.desc-and-faq a::attr(href)').get()
                categorytitle = re.sub(r"^/desc/", " ", categorytitle)
                # get description of the website for further processing
                description = site.css('div.title-and-desc div.site-descr::text').get()
                # Truncate leading and trailing whitespaces using regular expressions
                # as well as remove any other characters
                description = re.sub(r"^\s+|\s+$", " ", description)                
                yield{
                    'Category': categorytitle,
                    'WebsiteName': site.css('div.title-and-desc div.site-title::text').get(),
                    'WebsiteURL': site.css('div.title-and-desc a::attr(href)').get(),
                    'Description': description
                } 
        
        # Somepages don't have sites listed on them, but with other subcategories button to click on.
        # All the hrefs/ anchor items/ subcategories in the response page is followed by response.follow_all, with
        # parse method as callback.
        # By default, Scrapy performs Depth First Order(DFO) search.
        anchors = response.css('div.cat-item a')
        yield from response.follow_all(anchors, callback=self.parse)
    


                
                

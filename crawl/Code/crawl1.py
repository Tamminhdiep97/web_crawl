import scrapy
from scrapy.item import Item
from scrapy.http import Request



child_txt =['computer_science#compact'] #to check existance
child_queue =['computer_science#compact','artificial_intelligence#compact']  #first in first out, insert at tail


file_object = open("structure.txt","r",encoding="utf-8")
b=file_object.readline().strip('\n')
file_object.close()


def link_process(a):
    replace_string=a.replace(' ','_')
    return replace_string

def next_link():
    global b
    global child_queue
    link_url=child_queue
    return b+link_url[0]
   

class BrickSetSpider(scrapy.Spider):
    global child_txt
    global child_queue
    name = "brickset_spider"
    
    url=next_link()
    print(url)
    start_urls=[url]
    
    def parse(self, response):
        bd=[]
        set_selector=response.xpath("//table[1]")
        j=0
        for title in set_selector.css('.compact-topic'):
            j=j+1
            child = link_process(title.css('a ::text').get()+'#compact')
            bd.append(child)
        
        #crawl value
        child_txt.append(bd)
        title_page =response.css(".display-5::text").get()
        no_decendent = response.css(".card-body>p::text").getall()
        content = response.css(".card-text::text").get()
        link_wiki=response.css("#wikipedia::attr(href)").get()
        #print(child_txt)

        #pop head queue
        child_queue.pop(0)
        #process the next link
        next_url=next_link()

        yield Request(next_url)
  
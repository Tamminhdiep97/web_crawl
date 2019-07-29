import scrapy



child_txt =['computer_science#compact'] #to check existance
child_queue =['computer_science#compact','artificial_intelligence#compact']  #first in first out, insert at tail

def link_process(a):
    replace_string=a.replace(' ','_')
    return replace_string

def next_link(queue):
    queue.pop(0)
    if(len(queue)==0):
        return
    return queue[0]

class BrickSetSpider(scrapy.Spider):
    global child_txt
    global child_queue
    name = "brickset_spider"
    file_object = open("structure.txt","r",encoding="utf-8")
    b=file_object.readline().strip('\n')
    if(len(child_queue)==0): 
        exit()
    start_urls=[b+child_queue[0]]
        #print(start_urls)
    def parse(self, response):
        bd=[]
        set_selector=response.xpath("//table[1]")
        j=0
        for title in set_selector.css('.compact-topic'):
            j=j+1
            child = link_process(title.css('a ::text').get()+'#compact')
            bd.append(child)
            #yield {'title': title.css('a ::text').get()}
        child_txt = bd
            #print(child_txt)
        title_page =response.css(".display-5::text").get()
        no_decendent = response.css(".card-body>p::text").getall()
        content = response.css(".card-text::text").get()
        link_wiki=response.css("#wikipedia::attr(href)").get()
        print(title_page)
        child_queue.pop(0)
    BrickSetSpider(scrapy.Spider)
        #print(link_wiki)
"""
class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['https://cso.kmi.open.ac.uk/topics/computer_science#compact']
    def parse(self, response):
        set_selector='.compact-topic'
        for brick in response.css(set_selector):
            link = brick.css('a::attr(href)').extract_first()     
            yield scrapy.Request(link, callback=self.parse_attr)

    def parse_attr(self, response):
        file_write=open("crawl_data.txt","a",encoding="utf-8")
        file_write.write("name: "+ response.css('h1::text').extract_first()+'\n')
        file_write.write("description: " + response.css('.description::text').extract_first()+'\n')
        file_write.write("link: "+response.url + '\n')
        file_write.write("date: "+response.css('.time.left::text').extract_first()+'\n'+'\n')
"""
import scrapy
"""
def link_process(a):
    replace_string=a.replace(' ','_')
    return replace_string
file_object = open("structure.txt","r",encoding="utf-8")
a= file_object.read()
print(a)
"""
result =[]
class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls=['https://cso.kmi.open.ac.uk/topics/computer_science#compact']
    
    def parse(self, response):
        b=[]
        set_selector=response.xpath("//table[1]")
        i=0
        for title in set_selector.css('.compact-topic'):
            i=i+1
            print(i)
            a = title.css('a ::text').get()
            b.append(a)
            #yield {'title': title.css('a ::text').get()}
        global result
        result = b
        print(result)
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
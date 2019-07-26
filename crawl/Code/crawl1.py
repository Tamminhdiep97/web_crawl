import scrapy

def link_process(a):
    replace_string=a.replace(' ','_')
    return replace_string


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
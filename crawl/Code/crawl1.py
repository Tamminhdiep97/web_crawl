import scrapy
from scrapy.item import Item
from scrapy.http import Request
import time



child_txt =['computer_science'] #to check existance
child_queue =['computer_science#compact']  #first in first out, insert at tail


file_object = open("structure.txt","r",encoding="utf-8")
b=file_object.readline().strip('\n')
file_object.close()
file_write = open("result.txt","w",encoding="utf-8")

def link_process(a):
    replace_string=a.replace(' ','_')
    return replace_string

def next_link():
    global b
    global child_queue
    link_url=child_queue
    return b+link_url[0]

def process_NoneType(a):
    b=a
    if b is None:
        return " "
        print("true")
    else:
        return b

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"  
    url=next_link()
    start_urls=[url]
   
    def parse(self, response):
        global child_txt
        global child_queue
        global file_write

        child_list=" "
        set_selector=response.xpath("//table[1]")
       
        j=0
        for title in set_selector.css('.compact-topic'):
            
            child = title.css('a ::text').get()
            if j==0:
                child_list=child
            else:
                child_list=child_list+", "+child

            if child_txt.count(link_process(child))==0:  #if not exist, add to queue
                child_txt.append(link_process(child))
                child_queue.append(link_process(child)+'#compact')
            j=j+1
        #crawl value
        
        title_page = process_NoneType(response.css(".display-5::text").get())
        no_decendent = process_NoneType(response.css(".card-body>p::text").getall())
        content = process_NoneType(response.css(".card-text::text").get())
        #childof_ &_label
        """
        link_father = process_NoneType(set_selector.css("tr:last-child").getall())
        print(link_father)
        """
        link = response.url
        
        #External Resources
        link_resource=" "
        link_wiki = " "
        set_selector=response.xpath("//table[2]")
        link_external=process_NoneType(set_selector.css("span>a::attr(href)").getall()) #response.xpath("//a[contain(@id, wikipedia)]/")
        try:
            link_wiki = process_NoneType(response.xpath('//a[contains(@id, "wikipedia")]/@href')[2].get())   #link wiki
        except:
            pass
        
     
        if link_external != " ":
            for i in range(0,len(link_external)-1):
                link_resource = link_resource +", " + link_external[i]
        #experiment area

        selector_child = response.xpath('//div[contains(@id, "compact")]')
        selector_child_1 = selector_child.xpath('//table[1]/tbody/tr[th[contains(text(),"parent of")]]')
        selector_alternative_label = selector_child.xpath('//table[1]/tbody/tr[th[contains(text(),"alternative label")]]')
        selector_parent = selector_child.xpath('//table[1]/tbody/tr[th[contains(text(),"child of")]]')
        """for title in selector_child_1.css('.compact-topic'):
            child = title.css('a ::text').get()
            print(child)
        """
        for title in selector_parent.css('.compact-topic'):
            child = title.css('a ::text').get()
            print(child)


        #write to file
        file_write.write("Title: "+title_page)
        file_write.write('\n')
        file_write.write("Link: "+ link)
        file_write.write('\n')
        if len(no_decendent)<2:
            file_write.write("Number of Decendent"+" ")
        else:               
            file_write.write("Number of Decendent"+no_decendent[1])
        file_write.write('\n')                 
        file_write.write("content: "+content)
        file_write.write('\n')                 
        file_write.write("wiki: " +link_wiki)
        file_write.write('\n')                 
        file_write.write("Child list: " +child_list)
        file_write.write('\n')
        file_write.write("External_Resource: " + link_resource)
        file_write.write('\n\n\n')
        #pop head queue
        child_queue.pop(0)
        #process the next link
        next_url=next_link()
        #print(next_url)

        yield Request(next_url)

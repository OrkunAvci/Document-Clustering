import scrapy

class HashnodeBlogpostSpider(scrapy.Spider):
    name = 'hashnode_post'
    allowed_domains = ['hashnode.com']
    start_urls = ['https://hashnode.com/n/javascript']

    def parse(self, response):

        #post_url=response.css('a::attr(href)').getall()
        #post_header=response.css('a::text').getall()

        post_url=response.xpath('//div[@id="__next"]/div/div[2]/div[2]/div5/div/div[@class=bg-white]/div[2]/div/h1/a').getall()
        
        post_header=response.xpath('//div[@id="__next"]/div/div[2]/div[2]/div5/div/div[@class=bg-white]/div[2]/div/h1/a').getall()
        
         #//*[@id="__next"]/div/div[2]/div[2]/div[6]/div/div[1]/div[2]/div/h1
        
        raw_Data = zip(post_header,post_url)
      
        for item in raw_Data:
            scraped_info = {
                'post_header':item[0].strip(),
                'post_url':item[1].strip(),
            }

            yield scraped_info
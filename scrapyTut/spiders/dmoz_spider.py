import scrapy
from scrapyTut.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item


class rrdScraper(scrapy.Spider):
    name = "rrd"
    start_urls = ["https://www.renrendai.com/loginPage.action"]
    count = 1
    loan_url = 'http://www.renrendai.com/lend/detailPage.action?loanId='

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'j_username': 'andy135790@gmail.com', 'j_password': 'c870329y'},
            callback=self.after_login
        )

    def after_login(self, response):
        filename = 'after_login.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

        url = 'https://www.renrendai.com/account/index.action'
        yield scrapy.Request(self.loan_url + str(self.count), callback=self.start_scrap)


    def start_scrap(self, response):
        filename = 'start_scrap.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

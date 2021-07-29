import scrapy
import bs4
from ..items import RecruitingItem

class Spider_GetJobInfo(scrapy.Spider):
    name = 'GetJobsInfo'
    allowed_domains = ['www.jobui.com']
    start_urls = ['https://www.jobui.com/rank/company/']

    def parse(self, response):
        # 用BeautifulSoup解析response
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        ul_list = bs.find_all('ul', class_="textList flsty cfix")

        for ul in ul_list:
            a_list = ul.find_all('a')

            for a in a_list:
                company_id = a['href']
                url = 'https://www.jobui.com{id}jobs'.format(id=company_id)

                # 用yield语句把构造好的request对象传递给引擎。用scrapy.Request构造request对象。callback参数设置调用parse_GetJobInfo方法
                yield scrapy.Request(url, callback=self.parse_GetJobInfo)

    # 定义新的处理response的方法parse_GetJobInfo
    def parse_GetJobInfo(self, response):
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        company = bs.find(class_="company-banner-name").text
        datas = bs.find_all('div', class_="job-simple-content")

        for data in datas:
            # 实例化RecruitingItem这个类
            item = RecruitingItem()
            item['company'] = company
            item['position'] = data.find_all('div', class_="job-segmetation")[0].find('h3').text
            item['address'] = data.find_all('div', class_="job-segmetation")[1].find_all('span')[0].text
            item['detail'] = data.find_all('div', class_="job-segmetation")[1].find_all('span')[1].text
            # 用yield语句把item传递给引擎
            yield item

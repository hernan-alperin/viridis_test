from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.http import Request
import time
import sys
from indeed.items import IndeedItem
import lxml


class IndeedSpider(CrawlSpider):
  name = "indeed"
  allowed_domains = ["indeed.com"]
  start_urls = [
      "http://www.indeed.com/jobs?q=linux&l=Chicago&sort=date?",
      ]


  rules = (
      Rule(SgmlLinkExtractor(allow=('/jobs.q=linux&l=Chicago&sort=date$','q=linux&l=Chicago&sort=date&start=[0-9]+$',),deny=('/my/mysearches', '/preferences', '/advanced_search','/my/myjobs')), callback='parse_item', follow=False),

      )

  def parse_next_site(self, response):



    item = response.request.meta['item']
    item['source_url'] = response.url
    item['crawl_timestamp'] =  time.strftime('%Y-%m-%d %H:%M:%S')


    root = lxml.html.document_fromstring(response.body)
    target_element = ''


    # For some reason the summary will not match the lxml extracted text, figure out why
    # This solution is hacky
    summary = item['summary'][0][1:-5]

    for element in root.iter():
      if element.text:


        if summary in element.text:
          target_element = element
          break

    pass
    return item


  def parse_item(self, response):
    '''
    import pdb
    pdb.set_trace()
    '''


    self.log('\n Crawling  %s\n' % response.url)
    hxs = HtmlXPathSelector(response)
    sites = hxs.select("//div[@class='row ' or @class='row lastRow']")
    #sites = hxs.select("//div[@class='row ']")
    items = []

    #Skip top two sponsored ads
    for site in sites[2:]:
      item = IndeedItem(company='none')

      item['job_title'] = site.select('h2/a/@title').extract()
      link_url= site.select('h2/a/@href').extract()
      item['link_url'] = link_url
      item['crawl_url'] = response.url
      item['location'] = site.select("span[@itemprop='jobLocation']/span[@class='location']/span[@itemprop='addressLocality']/text()").extract()
      # Not all entries have a company
      company_name = site.select("span[@class='company']/span[@itemprop='name']/text()").extract()
      if company_name == []:
        item['company'] = [u'']
      else:
        item['company'] = company_name

      item['summary'] =site.select("table/tr/td/div/span[@class='summary']/text()").extract()
      #item['source'] = site.select("table/tr/td/span[@class='source']/text()").extract()
      item['found_date'] =site.select("table/tr/td/span[@class='date']/text()").extract()
      #item['source_url'] = self.get_source(link_url)

      if len(item['link_url']):
        request = Request("http://www.indeed.com" + item['link_url'][0], callback=self.parse_next_site)
        request.meta['item'] = item

        yield request


      items.append(item)

    return



SPIDER=IndeedSpider()

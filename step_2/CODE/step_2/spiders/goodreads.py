from datetime import datetime

import re
import scrapy
from scrapy.exceptions import CloseSpider


class GoodReadsSpider(scrapy.Spider):
    counter = 0
    max_count = 3000
    name = "goodreads"

    def start_requests(self):
        urls = [
            'https://www.goodreads.com/search?utf8=%E2%9C%93&q=fantasy&search_type=books',
            'https://www.goodreads.com/search?utf8=%E2%9C%93&q=adventure&search_type=books'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # visit each book page to scrape it's details
        books = response.xpath("//table[@class='tableList']/tr/td[1]/a/@href").extract()
        for book in books:
            yield scrapy.Request(url='https://www.goodreads.com' + book, callback=self.parse_book_page)

        # follow the pagination links to crawl all search results
        next_page = response.xpath("//a[@class='next_page']/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_book_page(self, response):
        if self.counter > self.max_count:
            raise CloseSpider('Finished scraping %s pages' % self.max_count)
        else:
            try:
                book_id = re.split("^(.*)(show\/)([0-9]*)(.*)$", response.url)[3]
                book_name = get_first(response.xpath("//h1[@id='bookTitle']/text()").extract())
                book_name_alt = get_first(response.xpath(
                    "//div[@id='bookDataBox']/div[@class='clearFloats']/div[@class='infoBoxRowItem']/text()").extract())
                author = get_first(response.xpath("//a[@class='authorName']/span/text()").extract())
                avg_rating = get_first(response.xpath("//span[@class='average']/text()").extract())
                book_format = get_first(response.xpath("//span[@itemprop='bookFormat']/text()").extract())
                count_pages = to_int(response.xpath("//span[@itemprop='numberOfPages']/text()").extract())
                publisher, date_published = extract_attrs(
                    response.xpath("//div[@id='details']/div[@class='row'][2]/text()").extract())
                self.counter += 1
                self.log('[INFO] Captured URL #{} : {}'.format(self.counter, response.url))
                yield {
                    'id': 'gr_%s' % book_id,
                    'book_name': book_name,
                    'book_name_alt': book_name_alt,
                    'author': author,
                    'avg_rating': avg_rating,
                    'book_format': book_format,
                    'count_pages': count_pages,
                    'publisher': publisher,
                    'date_published': date_published,
                    'source': response.url
                }
            except Exception as e:
                self.log('[WARN] Skipping URL: {}'.format(response.url))
                self.log(e)


def get_first(l):
    return l[0].strip() if len(l) else None


def to_int(param):
    if len(param):
        return int(param[0].strip().split(" ")[0])
    else:
        return -1


def extract_attrs(param):
    p_split = re.split("^(Published)(.*)( by )(.*)$", re.sub('\s+', ' ', param[0]).strip()) if len(param) else []
    if len(p_split) > 4:
        return p_split[4].strip(), to_date(p_split[2])
    else:
        return None, None


def to_date(param):
    if len(param):
        try:
            return datetime.strptime(re.sub(r'([0-9]+)(th|nd|rd|st)', r'\1', param).strip(), "%B %d %Y")
        except ValueError:
            return datetime.strptime(param.strip(), "%B %Y")
    else:
        return None

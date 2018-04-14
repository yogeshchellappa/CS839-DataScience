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
            'https://www.goodreads.com/search?q=Anne+Rice',
            'https://www.goodreads.com/search?q=Anne+McCaffrey',
            'https://www.goodreads.com/search?q=Bailey+Cates',
            'https://www.goodreads.com/search?q=Ben+Aaronovitch',
            'https://www.goodreads.com/search?q=Brandon+Sanderson',
            'https://www.goodreads.com/search?q=Brent+Weeks',
            'https://www.goodreads.com/search?q=C.+S.+Lewis',
            'https://www.goodreads.com/search?q=Carol+J.+Perry',
            'https://www.goodreads.com/search?q=Charlaine+Harris',
            'https://www.goodreads.com/search?page=2&q=Charlaine+Harris&tab=books',
            'https://www.goodreads.com/search?q=Chris+Gonnerman',
            'https://www.goodreads.com/search?q=Christopher+Paolini',
            'https://www.goodreads.com/search?q=Daniel+Abraham',
            'https://www.goodreads.com/search?q=Darynda+Jones',
            'https://www.goodreads.com/search?q=David+Dalglish',
            'https://www.goodreads.com/search?q=David+Eddings',
            'https://www.goodreads.com/search?page=2&q=David+Eddings&tab=books',
            'https://www.goodreads.com/search?q=David+Gemmell',
            'https://www.goodreads.com/search?page=2&q=David+Gemmell&tab=books',
            'https://www.goodreads.com/search?q=Dean+Koontz',
            'https://www.goodreads.com/search?page=2&q=Dean+Koontz&tab=books',
            'https://www.goodreads.com/search?q=Diana+Gabaldon',
            'https://www.goodreads.com/search?q=Douglas+Adams',
            'https://www.goodreads.com/search?q=E.E.+Knight',
            'https://www.goodreads.com/search?q=Gail+Z+Martin',
            'https://www.goodreads.com/search?q=George+R.+R.+Martin',
            'https://www.goodreads.com/search?page=2&q=George+R.+R.+Martin&tab=books',
            'https://www.goodreads.com/search?q=Glen+Cook',
            'https://www.goodreads.com/search?page=2&q=Glen+Cook&tab=books',
            'https://www.goodreads.com/search?q=Guy+Gavriel+Kay',
            'https://www.goodreads.com/search?q=Harry+Turtledove',
            'https://www.goodreads.com/search?page=2&q=Harry+Turtledove&tab=books',
            'https://www.goodreads.com/search?q=Heather+Graham',
            'https://www.goodreads.com/search?q=Ian+C.+Esslemont',
            'https://www.goodreads.com/search?q=J.+K.+Rowling',
            'https://www.goodreads.com/search?q=J.+R.+R.+Tolkien',
            'https://www.goodreads.com/search?page=2&q=J.+R.+R.+Tolkien&tab=books',
            'https://www.goodreads.com/search?page=2&q=J.+K.+Rowling&tab=books',
            'https://www.goodreads.com/search?q=James+Maxwell',
            'https://www.goodreads.com/search?q=James+Patterson',
            'https://www.goodreads.com/search?q=James+Rollins',
            'https://www.goodreads.com/search?q=Janny+Wurts',
            'https://www.goodreads.com/search?q=Jasper+Fforde',
            'https://www.goodreads.com/search?q=Jeff+Wheeler',
            'https://www.goodreads.com/search?q=Jim+Butcher',
            'https://www.goodreads.com/search?page=2&q=Jim+Butcher&tab=books',
            'https://www.goodreads.com/search?q=Joe+Abercrombie',
            'https://www.goodreads.com/search?q=Jonathan+Maberry',
            'https://www.goodreads.com/search?q=Juliet+Blackwell',
            'https://www.goodreads.com/search?q=K.+J.+Parker',
            'https://www.goodreads.com/search?q=Kate+Elliott',
            'https://www.goodreads.com/search?q=Kelley+Armstrong',
            'https://www.goodreads.com/search?q=Ken+Follett',
            'https://www.goodreads.com/search?q=Kevin+Hearne',
            'https://www.goodreads.com/search?q=Kim+Harrison',
            'https://www.goodreads.com/search?q=Kristen+Britain',
            'https://www.goodreads.com/search?q=L.+E.+Modesitt+Jr.',
            'https://www.goodreads.com/search?page=2&q=L.+E.+Modesitt+Jr.&tab=books',
            'https://www.goodreads.com/search?page=3&q=L.+E.+Modesitt+Jr.&tab=books',
            'https://www.goodreads.com/search?q=Laurell+K.+Hamilton',
            'https://www.goodreads.com/search?page=2&q=Laurell+K.+Hamilton&tab=books',
            'https://www.goodreads.com/search?q=Lincoln+Child',
            'https://www.goodreads.com/search?q=Lisa+Shearin',
            'https://www.goodreads.com/search?q=Lord+Dunsany',
            'https://www.goodreads.com/search?q=Lynn+Flewelling',
            'https://www.goodreads.com/search?q=Lynsay+Sands',
            'https://www.goodreads.com/search?page=2&q=Lynsay+Sands&tab=books',
            'https://www.goodreads.com/search?page=3&q=Lynsay+Sands&tab=books',
            'https://www.goodreads.com/search?q=Margaret+Weis',
            'https://www.goodreads.com/search?page=2&q=Margaret+Weis&tab=books',
            'https://www.goodreads.com/search?q=Mark+Lawrence',
            'https://www.goodreads.com/search?q=Max+McCoy',
            'https://www.goodreads.com/search?q=Melanie+Rawn',
            'https://www.goodreads.com/search?q=Mercedes+Lackey',
            'https://www.goodreads.com/search?page=2&q=Mercedes+Lackey&tab=books',
            'https://www.goodreads.com/search?q=Michael+A.+Stackpole',
            'https://www.goodreads.com/search?q=Michael+Crichton',
            'https://www.goodreads.com/search?q=Michael+J.+Sullivan',
            'https://www.goodreads.com/search?q=Michael+Moorcock',
            'https://www.goodreads.com/search?q=Michael+R.+Hicks',
            'https://www.goodreads.com/search?q=Michelle+Sagara',
            'https://www.goodreads.com/search?q=Miles+Cameron',
            'https://www.goodreads.com/search?q=Molly+Harrison',
            'https://www.goodreads.com/search?q=Myke+Cole',
            'https://www.goodreads.com/search?q=NK+Jemisin',
            'https://www.goodreads.com/search?q=Nalini+Singh',
            'https://www.goodreads.com/search?q=Naomi+Novik',
            'https://www.goodreads.com/search?q=Nicholas+Sansbury+Smith',
            'https://www.goodreads.com/search?q=Neil+Gaiman',
            'https://www.goodreads.com/search?q=Neal+Shusterman',
            'https://www.goodreads.com/search?q=Patricia+Briggs',
            'https://www.goodreads.com/search?q=Orson+Scott+Card',
            'https://www.goodreads.com/search?q=Oliver+Bowden',
            'https://www.goodreads.com/search?q=Rachel+Aaron',
            'https://www.goodreads.com/search?q=R.+A.+Salvatore',
            'https://www.goodreads.com/search?q=Piers+Anthony',
            'https://www.goodreads.com/search?q=Raymond+E+Feist',
            'https://www.goodreads.com/search?q=Rick+Riordan',
            'https://www.goodreads.com/search?q=Robert+Jordan',
            'https://www.goodreads.com/search?q=Robin+Hobb',
            'https://www.goodreads.com/search?q=Sarah+J+Maas',
            'https://www.goodreads.com/search?q=Selina+Fenech',
            'https://www.goodreads.com/search?q=Simon+R+Green',
            'https://www.goodreads.com/search?q=Stephen+King',
            'https://www.goodreads.com/search?page=2&q=Stephen+King&tab=books',
            'https://www.goodreads.com/search?page=3&q=Stephen+King&tab=books',
            'https://www.goodreads.com/search?q=Stephen+R+Donaldson',
            'https://www.goodreads.com/search?q=Terry+Brooks',
            'https://www.goodreads.com/search?q=Steven+Erikson',
            'https://www.goodreads.com/search?q=Terry+Goodkind',
            'https://www.goodreads.com/search?q=Terry+Pratchett',
            'https://www.goodreads.com/search?q=Tui+T+Sutherland',
            'https://www.goodreads.com/search?q=William+King'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # visit each book page to scrape it's details
        books = response.xpath("//table[@class='tableList']/tr/td[1]/a/@href").extract()
        for book in books:
            yield scrapy.Request(url='https://www.goodreads.com' + book, callback=self.parse_book_page)

        # follow the pagination links to crawl all search results
        #next_page = response.xpath("//a[@class='next_page']/@href").extract_first()
        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)

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

import scrapy

class VicVBASpider(scrapy.Spider):
    name = 'vic_vba_spider'
    allowed_domains = ['vba.biodiversity.vic.gov.au']
    start_urls = [
        'https://vba.biodiversity.vic.gov.au/'
    ]

    custom_settings = {
        'FEEDS': {
            'raw_scraped_articles.json': {
                'format': 'json',
                'encoding': 'utf8',
                'overwrite': True
            }
        }
    }

    def parse(self, response):
        # Look for links to records, reports, or downloads
        for link in response.css('a::attr(href)').getall():
            if 'record' in link or 'report' in link or 'download' in link:
                yield {
                    'url': response.urljoin(link),
                    'title': link.split('/')[-1],
                    'publication_date': None,
                    'body_text': None
                }
        if not response.css('a::attr(href)'):
            self.logger.warning('No accessible records or reports found. API or download may be required.') 
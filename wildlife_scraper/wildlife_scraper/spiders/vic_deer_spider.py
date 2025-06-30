import scrapy

class VicDeerSpider(scrapy.Spider):
    name = 'vic_deer_spider'
    allowed_domains = ['vdccn.org.au']
    start_urls = [
        'https://vdccn.org.au/'
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
        # Look for links to resources, news, or reports
        for link in response.css('a::attr(href)').getall():
            if 'resource' in link or 'news' in link or 'report' in link:
                yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        title = response.css('title::text').get()
        pub_date = None  # No clear date field on most pages
        body = ' '.join(response.css('main *::text').getall()).strip()
        yield {
            'url': response.url,
            'title': title,
            'publication_date': pub_date,
            'body_text': body
        } 
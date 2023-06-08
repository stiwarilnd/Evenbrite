import scrapy
import pandas as pd
import time


class EventLinkSpider(scrapy.Spider):
    name = 'event_links'
    categories = ['music', 'sports', 'technology']  # Add your desired categories here

    def start_requests(self):
        base_url = "https://www.eventbrite.com/d/az--phoenix/{category}--events/?page=1"

        for category in self.categories:
            url = base_url.format(category=category)
            yield scrapy.Request(url=url, callback=self.parse, meta={'category': category})

    def __init__(self):
        self.event_links = {}
    
    def parse(self, response):
        category = response.meta['category']
        links = response.css('a.event-card-link::attr(href)').getall()
        
        if category not in self.event_links:
            self.event_links[category] = []
        
        self.event_links[category].extend(links)

    def closed(self, reason):
        # Save event links to Excel
        df = pd.DataFrame(self.event_links)
        df = df.apply(lambda x: pd.Series(x.dropna().values))
        df.drop_duplicates(inplace=True)
        df.to_excel('event_links.xlsx', index=False)

        self.log(f'Saved event links to event_links.xlsx')


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(EventLinkSpider)
    process.start()

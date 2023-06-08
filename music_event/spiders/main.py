import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from database import *
import pandas as pd
class MainSpider(scrapy.Spider):
    name = 'main'

    def start_requests(self):
        # Read the Excel file
        df = pd.read_excel('event_links.xlsx')  # Replace 'file_path.xlsx' with the actual file path
        
        # Extract the URLs from the Excel file
        urls = df['LINK'].tolist()  # Assuming the URLs are in a column named 'URL'
        
        # Start scraping each URL
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('//h1[contains(@class, "event-title")]/text()').get()
        date_time = response.xpath('//p/span/text()').get()
        location = response.xpath('//p/strong/following-sibling::text()').get()
        price = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "conversion-bar__panel-info", " " ))]').get()
        url=response.url
        if title:
            title = title.strip()
            print('Title:', title)

        if date_time:
            date_time = date_time.strip().replace('Starts on', '')
            print('Date and Time:', date_time)
        if location:
            location = location.strip()
            print('location:', location)
        if price:
            price = price.strip()
            print('Price:', price)
        else:
            price=" "
            print('Price:', price)
        
        print("url:", url)
        
         # Insert the scraped data into the database
        sql = "INSERT INTO event (title, url, price, date_time, location) VALUES (%s, %s, %s, %s, %s)"
        data = (title, url, price, date_time, location)

        # Create a new database connection and cursor for each request
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='music_event',
            user='postgres',
            password='deol9646'
        )
        cursor = conn.cursor()

        cursor.execute(sql, data)

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()



        
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.settings.set('LOG_ENABLED', False)  # Disable logging
    process.crawl(MainSpider)
    process.start()









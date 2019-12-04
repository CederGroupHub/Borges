# Scraping AIP Papers
To use AIP spider, you should have the AIP account at first, and the account info need to
fill
the login information in the spiders code.

 
Run `scrapy craw aip_spider` to download metadata, which includes Volume, Published_Year, Issue, Journal, Publisher,
 Title, Article_HTML_Link, Article_PDF_Link, DOI, and Authors for each paper.


Run `scrapy craw aip_spider_full_text` to download full text as well as metadata of papers.



FROM python:3.9.7
WORKDIR /scraper
ADD . .
RUN pip install -r requirements.txt
CMD ["scrapy", "crawl", "tp-link"]



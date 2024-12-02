import asyncio
import random
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

import httpx
from bs4 import BeautifulSoup
from loguru import logger

class Crawler:
    def __init__(self, max_level=0, strict_mode=False, allowed_domains=None):
        self.crawled_urls = set()
        self.max_level = max_level
        self.strict_mode = strict_mode
        self.allowed_domains = allowed_domains if allowed_domains else []
        self.crawled_data = []
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        ]
        self.executor = ThreadPoolExecutor(max_workers=10)

    async def get_page(self, url):
        try:
            headers = {'User-Agent': random.choice(self.user_agents)}
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return response.content
                else:
                    logger.error(f"Error fetching {url}: Status code {response.status_code}")
                    return None
        except httpx.RequestError as e:
            logger.error(f"An error occurred while fetching {url}: {e}")
            return None

    def get_all_links(self, page, base_url):
        try:
            soup = BeautifulSoup(page, 'html.parser')
            links = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith('/'):
                    full_url = urljoin(base_url, href)
                    links.append(full_url)
                elif href:
                    links.append(href)
            return links
        except Exception as e:
            logger.error(f"Error parsing links: {e}")
            return []

    def get_title(self, page):
        try:
            soup = BeautifulSoup(page, 'html.parser')
            return soup.title.string
        except Exception as e:
            logger.error(f"Error parsing title: {e}")
            return "No Title"

    def is_allowed_domain(self, url):
        return any(allowed_domain in url for allowed_domain in self.allowed_domains)

    async def crawl(self, url, level=0):
        if level == self.max_level or url in self.crawled_urls:
            return
        if self.strict_mode and not self.is_allowed_domain(url):
            return
        self.crawled_urls.add(url)
        page = await self.get_page(url)
        if page is None:
            return
        title = self.get_title(page)
        content = page.decode('utf-8')
        self.crawled_data.append(
            {'url': url, 'title': title, 'content': content, 'html': page}
        )
        links = self.get_all_links(page, url)
        logger.info(f"Crawling {url} at level {level}")

        for link in links:
            if link and link not in self.crawled_urls:
                await self.crawl(link, level + 1)

    def get_crawled_data(self):
        return self.crawled_data

if __name__ == '__main__':
    crawler = Crawler(max_level=3, strict_mode=True, allowed_domains=['www.promptingguide.ai'])
    asyncio.run(crawler.crawl('https://www.promptingguide.ai/'))
    crawled_data = crawler.get_crawled_data()
    logger.info(f"Total pages crawled: {len(crawled_data)}")
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os

class NewsScraper:
    def __init__(self):
        self.sources = {
            'isna': 'https://www.isna.ir',
            'irna': 'https://www.irna.ir',
            'farsnews': 'https://www.farsnews.ir',
            'mehrnews': 'https://www.mehrnews.com',
            'tasnimnews': 'https://www.tasnimnews.com',
            'igedc': 'https://www.igedc.ir',
            'nigc': 'https://my.nigc.ir'
        }
        
        self.keywords = [
            'گاز', 'نفت', 'انرژی', 'پالایش', 'پتروشیمی',
            'صادرات گاز', 'واردات گاز', 'شرکت ملی گاز',
            'وزارت نفت', 'گازرسانی', 'خط لوله', 'میعانات',
            'توزیع گاز', 'انشعاب گاز', 'قطعی گاز'
        ]
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        self.archive_file = 'news_archive.json'
        self.load_archive()

    def load_archive(self):
        if os.path.exists(self.archive_file):
            with open(self.archive_file, 'r', encoding='utf-8') as f:
                self.archived_urls = set(json.load(f))
        else:
            self.archived_urls = set()

    def save_archive(self):
        with open(self.archive_file, 'w', encoding='utf-8') as f:
            json.dump(list(self.archived_urls), f, ensure_ascii=False, indent=2)

    def is_relevant(self, text):
        if not text:
            return False
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords)

    def scrape_isna(self):
        news_list = []
        try:
            response = requests.get(self.sources['isna'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = soup.find_all('div', class_='items')[:20]
            for article in articles:
                link_tag = article.find('a', href=True)
                title_tag = article.find('h3') or article.find('h2')
                
                if link_tag and title_tag:
                    title = title_tag.get_text(strip=True)
                    url = link_tag['href']
                    
                    if not url.startswith('http'):
                        url = self.sources['isna'] + url
                    
                    if self.is_relevant(title) and url not in self.archived_urls:
                        news_list.append({
                            'title': title,
                            'url': url,
                            'source': 'ایسنا'
                        })
                        self.archived_urls.add(url)
        except Exception as e:
            print(f"خطا در اسکرپ ایسنا: {e}")
        
        return news_list

    def scrape_irna(self):
        news_list = []
        try:
            response = requests.get(self.sources['irna'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = soup.find_all('div', class_='list-item')[:20]
            for article in articles:
                link_tag = article.find('a', href=True)
                title_tag = article.find('h3') or article.find('h2')
                
                if link_tag and title_tag:
                    title = title_tag.get_text(strip=True)
                    url = link_tag['href']
                    
                    if not url.startswith('http'):
                        url = self.sources['irna'] + url
                    
                    if self.is_relevant(title) and url not in self.archived_urls:
                        news_list.append({
                            'title': title,
                            'url': url,
                            'source': 'ایرنا'
                        })
                        self.archived_urls.add(url)
        except Exception as e:
            print(f"خطا در اسکرپ ایرنا: {e}")
        
        return news_list

    def scrape_farsnews(self):
        news_list = []
        try:
            response = requests.get(self.sources['farsnews'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = soup.find_all('div', class_='news-item')[:20]
            for article in articles:
                link_tag = article.find('a', href=True)
                title_tag = article.find('h3') or article.find('h2')
                
                if link_tag and title_tag:
                    title = title_tag.get_text(strip=True)
                    url = link_tag['href']
                    
                    if not url.startswith('http'):
                        url = self.sources['farsnews'] + url
                    
                    if self.is_relevant(title) and url not in self.archived_urls:
                        news_list.append({
                            'title': title,
                            'url': url,
                            'source': 'فارس'
                        })
                        self.archived_urls.add(url)
        except Exception as e:
            print(f"خطا در اسکرپ فارس: {e}")
        
        return news_list

    def scrape_mehrnews(self):
        news_list = []
        try:
            response = requests.get(self.sources['mehrnews'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = soup.find_all('div', class_='item')[:20]
            for article in articles:
                link_tag = article.find('a', href=True)
                title_tag = article.find('h3') or article.find('h2')
                
                if link_tag and title_tag:
                    title = title_tag.get_text(strip=True)
                    url = link_tag['href']
                    
                    if not url.startswith('http'):
                        url = self.sources['mehrnews'] + url
                    
                    if self.is_relevant(title) and url not in self.archived_urls:
                        news_list.append({
                            'title': title,
                            'url': url,
                            'source': 'مهر'
                        })
                        self.archived_urls.add(url)
        except Exception as e:
            print(f"خطا در اسکرپ مهر: {e}")
        
        return news_list

    def scrape_tasnimnews(self):
        news_list = []
        try:
            response = requests.get(self.sources['tasnimnews'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = soup.find_all('div', class_='list-item')[:20]
            for article in articles:
                link_tag = article.find('a', href=True)
                title_tag = article.find('h3') or article.find('h2')
                
                if link_tag and title_tag:
                    title = title_tag.get_text(strip=True)
                    url = link_tag['href']
                    
                    if not url.startswith('http'):
                        url = self.sources['tasnimnews'] + url
                    
                    if self.is_relevant(title) and url not in self.archived_urls:
                        news_list.append({
                            'title': title,
                            'url': url,
                            'source': 'تسنیم'
                        })
                        self.archived_urls.add(url)
        except Exception as e:
            print(f"خطا در اسکرپ تسنیم: {e}")
        
        return news_list

    def scrape_igedc(self):
        news_list = []
        try:
            response = requests.get(self.sources['igedc'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # سایت‌های شرکتی معمولاً خبرها رو توی بخش اخبار دارن
            articles = soup.find_all(['div', 'article'], class_=['news', 'post', 'item'])[:20]
            for article in articles:
                link_tag = article.find('a', href=True)
                title_tag = article.find(['h1', 'h2', 'h3', 'h4'])
                
                if link_tag and title_tag:
                    title = title_tag.get_text(strip=True)
                    url = link_tag['href']
                    
                    if not url.startswith('http'):
                        url = self.sources['igedc'] + url
                    
                    if url not in self.archived_urls:
                        news_list.append({
                            'title': title,
                            'url': url,
                            'source': 'شرکت توزیع گاز اصفهان'
                        })
                        self.archived_urls.add(url)
        except Exception as e:
            print(f"خطا در اسکرپ IGEDC: {e}")
        
        return news_list

    def scrape_nigc(self):
        news_list = []
        try:
            response = requests.get(self.sources['nigc'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # شرکت ملی گاز
            articles = soup.find_all(['div', 'article'], class_=['news', 'post', 'item'])[:20]
            for article in articles:
                link_tag = article.find('a', href=True)
                title_tag = article.find(['h1', 'h2', 'h3', 'h4'])
                
                if link_tag and title_tag:
                    title = title_tag.get_text(strip=True)
                    url = link_tag['href']
                    
                    if not url.startswith('http'):
                        url = self.sources['nigc'] + url
                    
                    if url not in self.archived_urls:
                        news_list.append({
                            'title': title,
                            'url': url,
                            'source': 'شرکت ملی گاز ایران'
                        })
                        self.archived_urls.add(url)
        except Exception as e:
            print(f"خطا در اسکرپ NIGC: {e}")
        
        return news_list

    def get_all_news(self):
        all_news = []
        
        print("در حال اسکرپ از ایسنا...")
        all_news.extend(self.scrape_isna())
        
        print("در حال اسکرپ از ایرنا...")
        all_news.extend(self.scrape_irna())
        
        print("در حال اسکرپ از فارس...")
        all_news.extend(self.scrape_farsnews())
        
        print("در حال اسکرپ از مهر...")
        all_news.extend(self.scrape_mehrnews())
        
        print("در حال اسکرپ از تسنیم...")
        all_news.extend(self.scrape_tasnimnews())
        
        print("در حال اسکرپ از شرکت توزیع گاز اصفهان...")
        all_news.extend(self.scrape_igedc())
        
        print("در حال اسکرپ از شرکت ملی گاز...")
        all_news.extend(self.scrape_nigc())
        
        
        self.save_archive()
        return all_news

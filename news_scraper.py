import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from config import NEWS_SOURCES, ARCHIVE_FILE


class NewsDatabase:
    def __init__(self, archive_file=ARCHIVE_FILE):
        self.archive_file = archive_file
        self.archive = self.load_archive()
    
    def load_archive(self):
        """بارگذاری آرشیو اخبار از فایل"""
        if os.path.exists(self.archive_file):
            try:
                with open(self.archive_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"خطا در بارگذاری آرشیو: {e}")
                return {}
        return {}
    
    def save_archive(self):
        """ذخیره آرشیو اخبار در فایل"""
        try:
            with open(self.archive_file, 'w', encoding='utf-8') as f:
                json.dump(self.archive, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطا در ذخیره آرشیو: {e}")
    
    def is_news_sent(self, news_id):
        """بررسی ارسال شدن خبر"""
        return news_id in self.archive
    
    def mark_as_sent(self, news_id, news_data):
        """علامت‌گذاری خبر به عنوان ارسال شده"""
        self.archive[news_id] = {
            'title': news_data.get('title', ''),
            'source': news_data.get('source', ''),
            'sent_at': datetime.now().isoformat()
        }
        self.save_archive()


class NewsScraper:
    def __init__(self):
        self.db = NewsDatabase()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_source(self, source_key, source_config):
        """اسکرپ یک منبع خبری"""
        news_list = []
        
        try:
            print(f"در حال اسکرپ {source_config['name']}...")
            response = requests.get(
                source_config['url'],
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            selectors = source_config['selectors']
            
            # یافتن اخبار
            news_items = soup.select(selectors['container'])
            
            for item in news_items[:5]:  # فقط 5 خبر اول
                try:
                    # استخراج عنوان
                    title_elem = item.select_one(selectors['title'])
                    title = title_elem.get_text(strip=True) if title_elem else None
                    
                    # استخراج لینک
                    link_elem = item.select_one(selectors['link'])
                    link = link_elem.get('href') if link_elem else None
                    
                    # کامل کردن لینک نسبی
                    if link and not link.startswith('http'):
                        base_url = '/'.join(source_config['url'].split('/')[:3])
                        link = base_url + link if link.startswith('/') else base_url + '/' + link
                    
                    # ایجاد شناسه منحصر به فرد
                    news_id = f"{source_key}_{hash(title)}"
                    
                    # بررسی ارسال نشده بودن
                    if title and link and not self.db.is_news_sent(news_id):
                        news_data = {
                            'id': news_id,
                            'title': title,
                            'link': link,
                            'source': source_config['name'],
                            'source_key': source_key
                        }
                        news_list.append(news_data)
                        
                except Exception as e:
                    print(f"خطا در پردازش خبر: {e}")
                    continue
            
            print(f"✅ {len(news_list)} خبر جدید از {source_config['name']}")
            
        except Exception as e:
            print(f"❌ خطا در اسکرپ {source_config['name']}: {e}")
        
        return news_list
    
    def scrape_all(self):
        """اسکرپ همه منابع خبری"""
        all_news = []
        
        for source_key, source_config in NEWS_SOURCES.items():
            news = self.scrape_source(source_key, source_config)
            all_news.extend(news)
        
        return all_news
    
    def mark_as_sent(self, news_id, news_data):
        """علامت‌گذاری خبر به عنوان ارسال شده"""
        self.db.mark_as_sent(news_id, news_data)


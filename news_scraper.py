import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

class NewsAggregator:
    def __init__(self):
        self.keywords = [
            'شرکت مهندسی و توسعه گاز ایران',
            'شرکت ملی گاز ایران',
            'مهندس بهنام میرزایی',
            'میرزایی',
            'خط لوله گاز',
            'ایستگاه تقویت فشار گاز',
            'صنعت گاز ایران',
            'گاز طبیعی ایران'
        ]
        
        self.sources = {
            'مهر': 'https://www.mehrnews.com',
            'ایسنا': 'https://www.isna.ir',
            'ایرنا': 'https://www.irna.ir',
            'شانا': 'https://www.shana.ir',
        }
    
    def search_mehr_news(self):
        """جستجو در خبرگزاری مهر"""
        news_list = []
        try:
            for keyword in self.keywords[:3]:  # سه کلیدواژه اصلی
                url = f"https://www.mehrnews.com/search?text={keyword}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    articles = soup.find_all('div', class_='item', limit=5)
                    
                    for article in articles:
                        try:
                            title_elem = article.find('a')
                            if title_elem:
                                title = title_elem.get_text(strip=True)
                                link = 'https://www.mehrnews.com' + title_elem.get('href')
                                
                                # چک کردن مرتبط بودن
                                if self._is_relevant(title):
                                    news_list.append({
                                        'title': title,
                                        'link': link,
                                        'source': 'مهر',
                                        'date': datetime.now(pytz.timezone('Asia/Tehran')).strftime('%Y-%m-%d')
                                    })
                        except:
                            continue
        except Exception as e:
            print(f"⚠️ خطا در جستجوی مهر: {e}")
        
        return news_list
    
    def search_isna_news(self):
        """جستجو در خبرگزاری ایسنا"""
        news_list = []
        try:
            for keyword in self.keywords[:3]:
                url = f"https://www.isna.ir/search?search={keyword}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    articles = soup.find_all('div', class_='news-img-desc', limit=5)
                    
                    for article in articles:
                        try:
                            title_elem = article.find('a')
                            if title_elem:
                                title = title_elem.get('title', '')
                                link = 'https://www.isna.ir' + title_elem.get('href')
                                
                                if self._is_relevant(title):
                                    news_list.append({
                                        'title': title,
                                        'link': link,
                                        'source': 'ایسنا',
                                        'date': datetime.now(pytz.timezone('Asia/Tehran')).strftime('%Y-%m-%d')
                                    })
                        except:
                            continue
        except Exception as e:
            print(f"⚠️ خطا در جستجوی ایسنا: {e}")
        
        return news_list
    
    def _is_relevant(self, text):
        """بررسی مرتبط بودن عنوان"""
        text_lower = text.lower()
        relevant_words = ['گاز', 'میرزایی', 'خط لوله', 'ایستگاه', 'شرکت ملی']
        return any(word in text_lower for word in relevant_words)
    
    def get_all_news(self):
        """جمع‌آوری از تمام منابع"""
        print("🔍 شروع جستجو در منابع...")
        all_news = []
        
        # جستجو در مهر
        mehr_news = self.search_mehr_news()
        print(f"✅ مهر: {len(mehr_news)} خبر")
        all_news.extend(mehr_news)
        
        # جستجو در ایسنا
        isna_news = self.search_isna_news()
        print(f"✅ ایسنا: {len(isna_news)} خبر")
        all_news.extend(isna_news)
        
        # حذف تکراری‌ها
        unique_news = []
        seen_links = set()
        for news in all_news:
            if news['link'] not in seen_links:
                seen_links.add(news['link'])
                unique_news.append(news)
        
        print(f"📊 مجموع اخبار یکتا: {len(unique_news)}")
        return unique_news

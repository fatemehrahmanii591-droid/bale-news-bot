import os
import requests
from datetime import datetime
from news_scraper import NewsScraper
from config import BALE_API_URL, MAX_MESSAGE_LENGTH


class BaleNewsBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.scraper = NewsScraper()
    
    def send_message(self, text):
        """ارسال پیام به بله"""
        url = BALE_API_URL.format(token=self.token, method='sendMessage')
        
        # تقسیم پیام‌های طولانی
        if len(text) > MAX_MESSAGE_LENGTH:
            chunks = [text[i:i+MAX_MESSAGE_LENGTH] 
                     for i in range(0, len(text), MAX_MESSAGE_LENGTH)]
            
            for chunk in chunks:
                data = {'chat_id': self.chat_id, 'text': chunk}
                try:
                    response = requests.post(url, json=data, timeout=30)
                    response.raise_for_status()
                    print(f"✅ بخشی از پیام ارسال شد")
                except Exception as e:
                    print(f"❌ خطا در ارسال پیام: {e}")
            return True
        else:
            data = {'chat_id': self.chat_id, 'text': text}
            try:
                response = requests.post(url, json=data, timeout=30)
                response.raise_for_status()
                print(f"✅ پیام با موفقیت ارسال شد")
                return response.json()
            except Exception as e:
                print(f"❌ خطا در ارسال پیام: {e}")
                return None
    
    def format_news_message(self, news_list):
        """فرمت کردن پیام خبری"""
        if not news_list:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            return f"📰 امروز خبر جدیدی در منابع یافت نشد.\n\n⏰ زمان بررسی: {now}"
        
        message = "🔔 *اخبار جدید صنعت گاز* 🔔\n"
        message += "━━━━━━━━━━━━━━━━━\n\n"
        
        for i, news in enumerate(news_list, 1):
            message += f"📌 *{i}. {news['title']}*\n"
            message += f"🔗 {news['link']}\n"
            message += f"📡 منبع: {news['source']}\n"
            message += "━━━━━━━━━━━━━━━━━\n\n"
        
        message += f"✅ تعداد کل: {len(news_list)} خبر"
        
        return message
    
    def run(self):
        """اجرای ربات"""
        print("🚀 شروع اسکرپ اخبار...")
        
        try:
            # اسکرپ اخبار
            news_list = self.scraper.scrape_all()
            
            if not news_list:
                print("ℹ️ خبر جدیدی برای ارسال وجود ندارد")
                # حتی اگه خبر نباشه، پیام بده
                message = self.format_news_message([])
                self.send_message(message)
                print("✅ پیام عدم وجود خبر ارسال شد")
                return
            
            print(f"📊 {len(news_list)} خبر جدید یافت شد")
            
            # فرمت و ارسال پیام
            message = self.format_news_message(news_list)
            result = self.send_message(message)
            
            if result:
                # علامت‌گذاری اخبار به عنوان ارسال شده
                for news in news_list:
                    self.scraper.mark_as_sent(news['id'], news)
                print("✅ اخبار با موفقیت ارسال و ذخیره شد")
            else:
                print("⚠️ پیام ارسال شد اما مشکلی در پاسخ وجود دارد")
                
        except Exception as e:
            print(f"❌ خطای کلی: {e}")
            error_msg = f"⚠️ خطا در اجرای ربات:\n{str(e)}"
            self.send_message(error_msg)


if __name__ == "__main__":
    # دریافت توکن و شناسه چت از متغیرهای محیطی
    TOKEN = os.getenv('BALE_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    
    if not TOKEN or not CHAT_ID:
        print("❌ خطا: BALE_TOKEN یا CHAT_ID تنظیم نشده است")
        exit(1)
    
    print(f"🤖 ربات با CHAT_ID={CHAT_ID} شروع به کار کرد")
    
    # اجرای ربات
    bot = BaleNewsBot(TOKEN, CHAT_ID)
    bot.run()
    
    print("🏁 اجرای ربات به پایان رسید")

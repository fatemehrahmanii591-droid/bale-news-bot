import os
import requests
from config import BALE_API_URL


class BaleMessageHandler:
    def __init__(self, token):
        self.token = token
        self.base_url = BALE_API_URL.format(token=self.token, method='')
    
    def send_message(self, chat_id, text):
        """ارسال پیام"""
        url = self.base_url + 'sendMessage'
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        }
        try:
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            print(f"✅ پیام به {chat_id} ارسال شد")
            return True
        except Exception as e:
            print(f"❌ خطا در ارسال پیام: {e}")
            return False
    
    def get_updates(self, offset=None):
        """دریافت پیام‌های جدید"""
        url = self.base_url + 'getUpdates'
        params = {'timeout': 30}
        if offset:
            params['offset'] = offset
        
        try:
            response = requests.get(url, params=params, timeout=35)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ خطا در دریافت پیام‌ها: {e}")
            return None
    
    def handle_message(self, message):
        """پردازش پیام"""
        chat_id = message['chat']['id']
        text = message.get('text', '')
        
        if text == '/start':
            welcome_msg = """
🤖 *سلام! به ربات خبری صنعت گاز خوش آمدید* 🤖

━━━━━━━━━━━━━━━━━

📰 این ربات هر روز آخرین اخبار صنعت گاز ایران رو برای شما ارسال می‌کنه.

🔔 *منابع خبری:*
• شانا (وزارت نفت)
• شرکت ملی گاز ایران

⏰ *زمان ارسال:* هر روز ساعت 09:00 صبح

━━━━━━━━━━━━━━━━━

✅ شما الان عضو کانال خبری شدید!

💬 برای پشتیبانی: @YourSupport
            """
            self.send_message(chat_id, welcome_msg.strip())
    
    def run(self):
        """اجرای هندلر"""
        print("🚀 شروع بررسی پیام‌های جدید...")
        
        updates = self.get_updates()
        
        if not updates or not updates.get('ok'):
            print("ℹ️ پیام جدیدی وجود ندارد")
            return
        
        results = updates.get('result', [])
        
        if not results:
            print("ℹ️ هیچ پیامی برای پردازش نیست")
            return
        
        print(f"📨 {len(results)} پیام جدید یافت شد")
        
        for update in results:
            if 'message' in update:
                self.handle_message(update['message'])


if __name__ == "__main__":
    TOKEN = os.getenv('BALE_TOKEN')
    
    if not TOKEN:
        print("❌ خطا: BALE_TOKEN تنظیم نشده است")
        exit(1)
    
    handler = BaleMessageHandler(TOKEN)
    handler.run()

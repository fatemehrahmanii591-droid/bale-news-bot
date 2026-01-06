import os
import json
from datetime import datetime
import pytz
import jdatetime
from news_scraper import NewsAggregator
from bale import Bot

def load_users():
    """بارگذاری لیست کاربران"""
    try:
        if os.path.exists('users.json'):
            with open('users.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return []

def load_sent_news():
    """بارگذاری اخبار ارسال‌شده"""
    try:
        if os.path.exists('news_archive.json'):
            with open('news_archive.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return []

def save_sent_news(news_list):
    """ذخیره اخبار ارسال‌شده"""
    try:
        with open('news_archive.json', 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        print("✅ آرشیو ذخیره شد")
        return True
    except Exception as e:
        print(f"❌ خطا در ذخیره: {e}")
        return False

def get_date_header():
    """تولید هدر تاریخ"""
    now_jalali = jdatetime.datetime.now()
    jalali_date = now_jalali.strftime('%Y/%m/%d')
    
    now_gregorian = datetime.now(pytz.timezone('Asia/Tehran'))
    gregorian_date = now_gregorian.strftime('%Y/%m/%d')
    
    return (
        f"🗓 *تاریخ امروز*\n"
        f"📅 شمسی: {jalali_date}\n"
        f"📅 میلادی: {gregorian_date}\n\n"
    )

def format_news_message(news_list):
    """فرمت پیام خبری"""
    message = "🌅 *صبح به‌خیر!*\n\n"
    message += get_date_header()
    
    if not news_list:
        message += (
            "📰 امروز خبر جدیدی در منابع یافت نشد.\n\n"
            "🔄 فردا دوباره بررسی می‌کنیم!"
        )
    else:
        message += f"📰 *{len(news_list)} خبر جدید از صنعت گاز:*\n\n"
        
        for idx, news in enumerate(news_list, 1):
            message += f"*{idx}. {news['title']}*\n"
            message += f"   📡 منبع: {news['source']}\n"
            message += f"   🔗 [مطالعه خبر]({news['link']})\n\n"
    
    now = datetime.now(pytz.timezone('Asia/Tehran'))
    message += f"\n⏰ ساعت ارسال: {now.strftime('%H:%M')}"
    
    return message

def main():
    print("🚀 شروع ربات خبری...")
    
    token = os.getenv('BALE_TOKEN')
    if not token:
        print("❌ توکن پیدا نشد!")
        return
    
    try:
        bot = Bot(token=token)
        print("✅ ربات ساخته شد")
        
        # بارگذاری کاربران
        users = load_users()
        if not users:
            print("⚠️ هیچ کاربری ثبت‌نام نکرده!")
            return
        
        print(f"👥 تعداد کاربران: {len(users)}")
        
        # جمع‌آوری اخبار
        print("🔍 جستجوی اخبار...")
        aggregator = NewsAggregator()
        all_news = aggregator.get_all_news()
        print(f"📊 تعداد کل اخبار: {len(all_news)}")
        
        # فیلتر اخبار جدید
        sent_news = load_sent_news()
        sent_links = {news['link'] for news in sent_news}
        new_news = [news for news in all_news if news['link'] not in sent_links]
        print(f"🆕 اخبار جدید: {len(new_news)}")
        
        # آماده‌سازی پیام
        message_text = format_news_message(new_news)
        
        # ارسال به همه کاربران
        success_count = 0
        for user_id in users:
            try:
                bot.send_message(
                    chat_id=user_id,
                    text=message_text,
                    parse_mode='markdown'
                )
                success_count += 1
                print(f"✅ ارسال به {user_id}")
            except Exception as e:
                print(f"❌ خطا در ارسال به {user_id}: {e}")
        
        print(f"📤 ارسال موفق: {success_count}/{len(users)}")
        
        # به‌روزرسانی آرشیو
        if new_news:
            sent_news.extend(new_news)
            # نگه‌داری 1000 خبر آخر
            if len(sent_news) > 1000:
                sent_news = sent_news[-1000:]
            save_sent_news(sent_news)
        
        print("🎉 کار تمام شد!")
        
    except Exception as e:
        print(f"❌ خطای کلی: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

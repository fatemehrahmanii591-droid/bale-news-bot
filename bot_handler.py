import os
import json
from bale import Bot, Update
from datetime import datetime
import pytz
import jdatetime

def load_users():
    """بارگذاری لیست کاربران"""
    try:
        if os.path.exists('users.json'):
            with open('users.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return []

def save_users(users):
    """ذخیره لیست کاربران"""
    try:
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ خطا در ذخیره کاربران: {e}")
        return False

def get_greeting_message():
    """تولید پیام صبح‌بخیر با تاریخ"""
    # تاریخ شمسی
    now_jalali = jdatetime.datetime.now()
    jalali_date = now_jalali.strftime('%Y/%m/%d')
    jalali_day = now_jalali.strftime('%A')
    
    # تاریخ میلادی
    now_gregorian = datetime.now(pytz.timezone('Asia/Tehran'))
    gregorian_date = now_gregorian.strftime('%Y/%m/%d')
    gregorian_day = now_gregorian.strftime('%A')
    
    # ترجمه روز
    days_fa = {
        'Saturday': 'شنبه',
        'Sunday': 'یکشنبه',
        'Monday': 'دوشنبه',
        'Tuesday': 'سه‌شنبه',
        'Wednesday': 'چهارشنبه',
        'Thursday': 'پنج‌شنبه',
        'Friday': 'جمعه'
    }
    
    return (
        f"🌅 *صبح به‌خیر!*\n\n"
        f"📅 امروز {days_fa.get(gregorian_day, gregorian_day)}:\n"
        f"🗓 تاریخ شمسی: {jalali_date}\n"
        f"🗓 تاریخ میلادی: {gregorian_date}\n\n"
        f"☕️ روز خوبی داشته باشید!"
    )

def main():
    print("🤖 شروع پردازش پیام‌ها...")
    
    token = os.getenv('BALE_TOKEN')
    if not token:
        print("❌ توکن پیدا نشد!")
        return
    
    try:
        bot = Bot(token=token)
        users = load_users()
        
        # دریافت آپدیت‌های جدید
        updates = bot.get_updates()
        
        for update in updates:
            if update.message and update.message.text:
                chat_id = str(update.message.chat.id)
                text = update.message.text.strip()
                
                print(f"📨 پیام از {chat_id}: {text}")
                
                # دستور /start
                if text.lower() == '/start':
                    # اضافه کردن کاربر
                    if chat_id not in users:
                        users.append(chat_id)
                        save_users(users)
                        print(f"✅ کاربر جدید: {chat_id}")
                    
                    # پیام خوش‌آمدگویی
                    welcome_msg = (
                        "🎉 *خوش آمدید به ربات خبری گاز ایران!*\n\n"
                        "✅ شما با موفقیت ثبت‌نام شدید!\n\n"
                        "از این پس هر روز:\n"
                        "📰 آخرین اخبار صنعت گاز\n"
                        "🏢 اخبار شرکت ملی گاز و شرکت مهندسی و توسعه گاز\n"
                        "👨‍💼 اخبار مرتبط با مهندس میرزایی\n"
                        "⚡️ اخبار خطوط لوله و ایستگاه‌های تقویت فشار\n\n"
                        "برای شما ارسال می‌شود!\n\n"
                        f"{get_greeting_message()}"
                    )
                    
                    bot.send_message(
                        chat_id=chat_id,
                        text=welcome_msg,
                        parse_mode='markdown'
                    )
                    print(f"✅ پیام خوش‌آمدگویی ارسال شد به {chat_id}")
        
        print(f"🎯 تعداد کاربران ثبت‌شده: {len(users)}")
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

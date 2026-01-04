NEWS_SOURCES = {
    'nigc': {
        'name': 'شرکت ملی گاز ایران',
        'url': 'https://www.nigc.ir/News',
        'selectors': {
            'container': 'div.news-item',
            'title': 'h3.news-title',
            'link': 'a',
            'date': 'span.news-date'
        }
    },
    'gedco': {
        'name': 'شرکت گاز استان گیلان',
        'url': 'https://www.gedco.ir/News',
        'selectors': {
            'container': 'div.news-box',
            'title': 'h4.title',
            'link': 'a',
            'date': 'span.date'
        }
    },
    'igc': {
        'name': 'شرکت بین‌المللی گاز ایران',
        'url': 'https://www.igc.ir/news',
        'selectors': {
            'container': 'article.news-item',
            'title': 'h2.entry-title',
            'link': 'a.news-link',
            'date': 'time.published'
        }
    },
    'shana': {
        'name': 'شانا - خبرگزاری نفت',
        'url': 'https://www.shana.ir/news',
        'selectors': {
            'container': 'div.item-news',
            'title': 'h3.title-news',
            'link': 'a.link-news',
            'date': 'span.date-news'
        }
    },
    'irangas': {
        'name': 'ایران گاز',
        'url': 'https://www.irangas.org.ir/news',
        'selectors': {
            'container': 'div.news-card',
            'title': 'h4.card-title',
            'link': 'a.card-link',
            'date': 'span.card-date'
        }
    }
}

# تنظیمات ربات
BALE_API_URL = "https://tapi.bale.ai/bot{token}/{method}"
MAX_MESSAGE_LENGTH = 4000
ARCHIVE_FILE = "news_archive.json"


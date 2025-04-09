import feedparser
import re
import nltk
from collections import Counter, defaultdict
from datetime import datetime
from nltk.corpus import stopwords
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

# Download stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# RSS Feeds
rss_feeds = [
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "https://www.thehindu.com/news/national/feeder/default.rss",
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "http://feeds.reuters.com/reuters/topNews",
    "https://www.ndtv.com/rss",
    "https://www.theguardian.com/world/rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "https://www.hindustantimes.com/rss/topnews/rssfeed.xml"
]

all_articles = []
keyword_to_articles = defaultdict(list)

# Step 1: Collect and Clean
for feed_url in rss_feeds:
    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        title = entry.get("title", "N/A")
        link = entry.get("link", "N/A")
        pub_date = entry.get("published", entry.get("updated", "N/A"))
        raw_description = entry.get("summary", "N/A")
        clean_description = re.sub(r'<[^>]+>', '', raw_description).strip()

        words = re.findall(r'\b[a-z]{4,}\b', clean_description.lower())
        filtered_words = [word for word in words if word not in stop_words]
        word_counts = Counter(filtered_words)
        top_keywords = [word.capitalize() for word, _ in word_counts.most_common(5)]

        article = {
            "title": title.strip(),
            "description": clean_description,
            "link": link.strip(),
            "published": pub_date.strip(),
            "keywords": top_keywords,
            "common_match": "NA"
        }

        all_articles.append(article)
        for kw in top_keywords:
            keyword_to_articles[kw].append(len(all_articles) - 1)

# Step 2: Match Articles Based on Common Keywords
for i, article in enumerate(all_articles):
    common_keywords = set()
    for kw in article["keywords"]:
        if len(keyword_to_articles[kw]) > 1:
            common_keywords.add(kw)
    if common_keywords:
        article["common_match"] = ", ".join(sorted(common_keywords))

# Step 3: Export to Excel with Highlighted Headers
wb = Workbook()
ws = wb.active
ws.title = "Top News"

# Define headers
headers = ["Title", "Description", "Link", "Published Date", "Top Keywords", "Common Keyword Match"]
ws.append(headers)

# Style header
header_fill = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")  # Light Blue
bold_font = Font(bold=True)

for col_num, column_title in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col_num)
    cell.fill = header_fill
    cell.font = bold_font

# Fill rows
for article in all_articles:
    ws.append([
        article["title"],
        article["description"],
        article["link"],
        article["published"],
        ", ".join(article["keywords"]),
        article["common_match"]
    ])

# Save Excel file
excel_filename = f"top_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
wb.save(excel_filename)

print(f"✅ Excel created with {len(all_articles)} articles. Saved as '{excel_filename}'")

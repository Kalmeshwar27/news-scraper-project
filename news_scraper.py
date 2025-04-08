import feedparser
import csv
import re
import nltk
from collections import Counter
from datetime import datetime
from nltk.corpus import stopwords

# Download stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# RSS feeds from top news sources
rss_feeds = [
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "https://www.thehindu.com/news/national/feeder/default.rss",
    "http://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
    "https://www.aljazeera.com/xml/rss/all.xml"
]

all_news = []

for feed_url in rss_feeds:
    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        title = entry.get("title", "N/A")
        link = entry.get("link", "N/A")
        pub_date = entry.get("published", entry.get("updated", "N/A"))
        description = entry.get("summary", "N/A")

        # Clean and process description text
        words = re.findall(r'\b[a-z]{4,}\b', description.lower())
        filtered_words = [word for word in words if word not in stop_words]
        word_counts = Counter(filtered_words)
        top_keywords = [word.capitalize() for word, _ in word_counts.most_common(5)]
        keywords = ", ".join(top_keywords) if top_keywords else "N/A"

        all_news.append([
            title.strip(),
            description.strip(),
            link.strip(),
            pub_date.strip(),
            keywords
        ])

# Save to CSV
csv_filename = f"top_news_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
with open(csv_filename, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Description", "Link", "Published Date", "Top Keywords"])
    writer.writerows(all_news)

print(f"✅ CSV created with {len(all_news)} articles. Saved as '{csv_filename}'")

import feedparser

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

print("Checking how many articles are returned from each RSS feed...\n")

for url in rss_feeds:
    feed = feedparser.parse(url)
    print(f"{url}\n➡️  Articles found: {len(feed.entries)}\n")

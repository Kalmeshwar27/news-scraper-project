import requests
import csv
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords


nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

API_KEY = 'pub_785021193f66176e5970a0321729dcba4ad02'
url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&language=en&country=in"

response = requests.get(url)
data = response.json()

news_data = []

for article in data.get("results", []):
    title = article.get("title") or "N/A"
    summary = article.get("description") or article.get("content") or article.get("title") or "N/A"

    link = article.get("link") or "N/A"
    date = article.get("pubDate") or "N/A"

    short_summary = summary.strip()
    if len(short_summary) > 200:
        short_summary = short_summary[:197] + "..."

    
    words = re.findall(r'\b[a-z]{4,}\b', summary.lower())
    filtered_words = [word for word in words if word not in stop_words]

   
    word_counts = Counter(filtered_words)
    top_words = [word.capitalize() for word, _ in word_counts.most_common(5)]

    news_data.append([
        link.strip(),
        title.strip().title(),
        short_summary,
        date.strip(),
        ", ".join(top_words)
    ])


with open('news_output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['News URL', 'Title', 'Summary (Shortened)', 'Published Date', 'Top 5 Keywords'])
    writer.writerows(news_data)

print(f"✅ CSV created with {len(news_data)} rows.")

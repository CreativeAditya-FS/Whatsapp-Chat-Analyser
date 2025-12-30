from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import os

extract = URLExtract()

# -------------------- BASIC STATS --------------------
def fetch_stats(selected_user, df):

    if df.empty:
        return 0, 0, 0, 0

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for msg in df['message']:
        words.extend(msg.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for msg in df['message']:
        links.extend(extract.find_urls(msg))

    return num_messages, len(words), num_media_messages, len(links)

# -------------------- BUSY USERS --------------------
def most_busy_users(df):
    if df.empty:
        return pd.Series(dtype=int), pd.DataFrame()

    x = df['user'].value_counts().head()
    percent_df = round(
        (df['user'].value_counts() / df.shape[0]) * 100, 2
    ).reset_index()
    percent_df.columns = ['name', 'percent']

    return x, percent_df

# -------------------- WORDCLOUD --------------------
def create_wordcloud(selected_user, df):

    stop_path = "stop_hinglish.txt"
    if not os.path.exists(stop_path):
        return None

    with open(stop_path, 'r', encoding='utf-8') as f:
        stop_words = f.read().split()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[
        (df['user'] != 'group_notification') &
        (df['message'] != '<Media omitted>\n')
    ]

    if temp.empty:
        return None

    def clean_msg(msg):
        return " ".join([w for w in msg.lower().split() if w not in stop_words])

    text = " ".join(temp['message'].apply(clean_msg))

    if not text.strip():
        return None

    wc = WordCloud(width=500, height=500, background_color='white')
    return wc.generate(text)

# -------------------- COMMON WORDS --------------------
def most_common_words(selected_user, df):

    if df.empty:
        return pd.DataFrame()

    stop_path = "stop_hinglish.txt"
    if not os.path.exists(stop_path):
        return pd.DataFrame()

    with open(stop_path, 'r', encoding='utf-8') as f:
        stop_words = f.read().split()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    words = []
    for msg in df['message']:
        for w in msg.lower().split():
            if w not in stop_words:
                words.append(w)

    return pd.DataFrame(Counter(words).most_common(20))

# -------------------- EMOJI ANALYSIS --------------------
def emoji_helper(selected_user, df):

    if df.empty:
        return pd.DataFrame()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])

    return pd.DataFrame(Counter(emojis).most_common(10))

# -------------------- TIMELINES --------------------
def monthly_timeline(selected_user, df):

    if df.empty:
        return pd.DataFrame()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = (
        df.groupby(['year', 'month_num', 'month'])['message']
        .count()
        .reset_index()
    )

    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):

    if df.empty:
        return pd.DataFrame()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.groupby('only_date')['message'].count().reset_index()

# -------------------- ACTIVITY MAPS --------------------
def week_activity_map(selected_user, df):

    if df.empty:
        return pd.Series(dtype=int)

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):

    if df.empty:
        return pd.Series(dtype=int)

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):

    if df.empty:
        return pd.DataFrame()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

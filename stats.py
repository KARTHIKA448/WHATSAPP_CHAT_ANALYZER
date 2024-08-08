from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji
import matplotlib.pyplot as plt

extract = URLExtract()


def fetchstats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['Message']:
        words.extend(message.split())

    mediaommitted = df[df['Message'] == '<Media omitted>']
    links = [link for message in df['Message'] for link in extract.find_urls(message)]

    return num_messages, len(words), mediaommitted.shape[0], len(links)


def fetchbusyuser(df):
    df = df[df['User'] != 'Group Notification']
    count = df['User'].value_counts().head()
    newdf = pd.DataFrame((df['User'].value_counts() / df.shape[0]) * 100)
    return count, newdf


def createwordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    # Convert 'Message' column to strings
    df['Message'] = df['Message'].astype(str)

    # Check if there are any words to create a word cloud
    text = df['Message'].str.cat(sep=" ")
    if not text.strip():
        return None

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(text)
    return df_wc.to_array()


def getcommonwords(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # Remove media messages and group notifications
    temp = df[df['Message'] != '<Media omitted>\n']
    temp = temp[temp['Message'] != 'This message was deleted\n']

    # Create a list of words
    words = []
    for message in temp['Message']:
        words.extend(message.split())

    # Count the most common words
    common_words = Counter(words).most_common(20)
    common_df = pd.DataFrame(common_words, columns=['Word', 'Count'])

    return common_df


def get_most_used_emoji(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # Extract emojis from messages
    emojis = [c for message in df['Message'] for c in message if c in emoji.EMOJI_DATA]
    emoji_counts = Counter(emojis)

    # Find the most used emoji
    if emoji_counts:
        most_used_emoji = max(emoji_counts, key=emoji_counts.get)
        return most_used_emoji, emoji_counts[most_used_emoji]
    else:
        return None, 0


def getemojistats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_counts = pd.Series(emojis).value_counts().reset_index()
    emoji_counts.columns = ['Emoji', 'Count']

    return emoji_counts


def monthtimeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # Ensure 'Date' is in datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])  # Remove rows where date conversion failed

    df['Month'] = df['Date'].dt.to_period('M')
    timeline = df.groupby('Month').count()['Message'].reset_index()
    timeline['Time'] = timeline['Month'].astype(str)

    return timeline


def weekactivitymap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # Ensure that 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Create a new column for day of the week
    df['Day_of_Week'] = df['Date'].dt.day_name()

    # Count the number of messages for each day of the week
    activity_map = df['Day_of_Week'].value_counts().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ], fill_value=0)

    return activity_map


def monthactivitymap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # Ensure that 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Create a new column for month of the year
    df['Month'] = df['Date'].dt.month_name()

    # Count the number of messages for each month
    activity_map = df['Month'].value_counts().reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ], fill_value=0)

    return activity_map

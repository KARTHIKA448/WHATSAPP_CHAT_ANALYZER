import streamlit as st
import numpy as np
import seaborn as sn
import pandas as pd
import re

def gettimeanddate(string):
    string = string.split(',')
    date, time = string[0], string[1]
    time = time.split('-')
    time = time[0].strip()

    return date+" "+time

def getstring(text):
    return text.split('\n')[0]

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:am|pm)\s-\s'

    row = data.split('\n')
    data = [data.replace('\u202f', '') for data in row]

    all_messages = []
    all_dates = []

    for cleaned_data in data:
        # Extract dates
        dates = re.findall(pattern, cleaned_data)
        all_dates.extend(dates)

        # Extract messages
        messages = re.split(pattern, cleaned_data)[1:]

        all_messages.extend(messages)

    df = pd.DataFrame({'user_messages': all_messages, 'message_date': all_dates})

    df['message_date'] = df['message_date'].apply(lambda text: gettimeanddate(text))
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_messages']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notification')
            messages.append(entry[0])

    df['User'] = users
    df['message'] = messages

    df['message'] = df['message'].apply(lambda text: getstring(text))

    df = df.drop(['user_messages'], axis=1)
    df = df[['message', 'date', 'User']]

    df = df.rename(columns={'message': 'Message', 'date': 'Date'})

    df['Only date'] = pd.to_datetime(df['Date']).dt.date
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    df['Month_num'] = pd.to_datetime(df['Date']).dt.month
    df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
    df['Day'] = pd.to_datetime(df['Date']).dt.day
    df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()
    df['Hour'] = pd.to_datetime(df['Date']).dt.hour
    df['Minute'] = pd.to_datetime(df['Date']).dt.minute

    return df


def preprocess(data):
    messages = []
    dates = []
    users = []

    for line in data.split('\n'):
        try:
            if line:
                # Assuming the format: 'date - user: message'
                date_part, rest = line.split(' - ', 1)
                user_part, message = rest.split(': ', 1)

                # Append data to lists
                dates.append(date_part)
                users.append(user_part)
                messages.append(message)
        except ValueError as e:
            # Handle lines that do not conform to the expected format
            print(f"Skipping line due to format error: {line}")
            print(f"Error: {e}")

    df = pd.DataFrame({'Date': dates, 'User': users, 'Message': messages})

    # Convert 'Date' column to datetime format
    try:
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y, %H:%M')
    except Exception as e:
        print(f"Date conversion error: {e}")

    return df
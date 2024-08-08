import streamlit as st
import preprocess
import stats
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.sidebar.title("WhatsApp Chat Analyzer")

# Upload file
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)

    # Show the dataframe
    if st.checkbox("Show DataFrame"):
        st.dataframe(df)

    # Fetch unique users
    user_list = df['User'].unique().tolist()

    # Remove 'Group Notification'
    if 'Group Notification' in user_list:
        user_list.remove('Group Notification')

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)
    st.title("WhatsApp Chat Analysis for " + selected_user)

    if st.sidebar.button("Show Analysis"):
        # Basic stats
        num_messages, num_words, media_omitted, links = stats.fetchstats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total No.of Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(media_omitted)
        with col4:
            st.header("Total Links Shared")
            st.title(links)

        # Busiest users
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            busycount, newdf = stats.fetchbusyuser(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(busycount.index, busycount.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(newdf)

        # Word Cloud
        st.title('Word Cloud')
        df_img = stats.createwordcloud(selected_user, df)
        if df_img is not None:
            fig, ax = plt.subplots()
            ax.imshow(df_img)
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.write("No valid words to display a word cloud.")

        # Most common words
        most_common_df = stats.getcommonwords(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df['Word'], most_common_df['Count'])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # Emoji Analysis
        emoji_df = stats.getemojistats(selected_user, df)
        emoji_df.columns = ['Emoji', 'Count']
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            emojicount = list(emoji_df['Count'])
            perlist = [(i / sum(emojicount)) * 100 for i in emojicount]
            emoji_df['Percentage use'] = np.array(perlist)
            st.dataframe(emoji_df)

        # Most used emoji by the user
        most_used_emoji, count = stats.get_most_used_emoji(selected_user, df)
        st.title("Most Used Emoji")
        st.write(f"The most used emoji by {selected_user} is: {most_used_emoji} used {count} times")

        # Monthly timeline
        st.title("Monthly Timeline")
        time = stats.monthtimeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(time['Time'], time['Message'], color='green')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)

        # Activity maps
        st.title("Activity Maps")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = stats.weekactivitymap(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = stats.monthactivitymap(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

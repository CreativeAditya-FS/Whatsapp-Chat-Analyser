import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Whatsapp Chat Analyzer")
st.sidebar.title("Whatsapp Chat Analyzer")
st.sidebar.text("Minor Project")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8-sig")

    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # -------------------- TOP STATS --------------------
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Messages", num_messages)
        col2.metric("Total Words", words)
        col3.metric("Media Shared", num_media_messages)
        col4.metric("Links Shared", num_links)

        # -------------------- MONTHLY TIMELINE --------------------
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)

        if not timeline.empty:
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        else:
            st.warning("No data available")

        # -------------------- DAILY TIMELINE --------------------
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)

        if not daily_timeline.empty:
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        else:
            st.warning("No data available")

        # -------------------- ACTIVITY MAP --------------------
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # -------------------- HEATMAP --------------------
        st.title("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)

        if not user_heatmap.empty:
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Not enough data for heatmap")

        # -------------------- BUSY USERS --------------------
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # -------------------- WORDCLOUD --------------------
        st.title("Wordcloud")
        wc = helper.create_wordcloud(selected_user, df)

        if wc:
            fig, ax = plt.subplots()
            ax.imshow(wc)
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.warning("No words available")

        # -------------------- MOST COMMON WORDS --------------------
        st.title("Most Common Words")
        common_df = helper.most_common_words(selected_user, df)

        if not common_df.empty:
            fig, ax = plt.subplots()
            ax.barh(common_df[0], common_df[1])
            st.pyplot(fig)
        else:
            st.warning("No common words")

        # -------------------- EMOJI ANALYSIS --------------------
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        if not emoji_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1], labels=emoji_df[0], autopct="%0.2f")
                st.pyplot(fig)
        else:
            st.warning("No emojis found")

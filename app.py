import streamlit as st
import matplotlib.pyplot as plt
import analysis

st.set_page_config(layout='wide')
st.sidebar.markdown("<h1 style='text-align: center;'>Chat Analyzer</h1>", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = analysis.preprocess(data)
    
    # FILTER BY USER BUTTON 
    user_list = analysis.unique_users(df)
    selected_user = st.sidebar.selectbox('Filter by user', user_list)

    # SHOW ANALYSIS BUTTON
    if st.sidebar.button('Show Analysis'):

        # TOTAL STATS SECTION
        st.markdown("<h1 style='text-align: center;'>Total Statistics</h1>", unsafe_allow_html=True)
        num_mess, words, num_media, num_deleted = analysis.fetch_stats(selected_user, df)
        
        col1, col2, col3, col4= st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(num_mess)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Messages')
            st.title(num_media)
        with col4:
            st.header('Deleted Messages')
            st.title(num_deleted)

        # TOP USERS SECTION
        if selected_user=='Overall':
            st.markdown("<h1 style='text-align: center;'>Top Users</h1>", unsafe_allow_html=True)
            x, percent_df = analysis.top_users(df)
            fig, ax = plt.subplots()
            bars = ax.bar(x.index, x.values, color='steelblue')
            ax.bar_label(bars)
            plt.xticks(rotation='vertical')
            plt.xlabel('Users')
            plt.ylabel('Messages')
            st.pyplot(fig)

            col1, col2, col3 = st.columns([1,8,1])  # for centering the dataframe
            with col1:
                st.title('')
            with col2:
                st.dataframe(percent_df)
            with col3:
                st.title('')
                
        # MONTHLY TIMELINE
        st.markdown("<h1 style='text-align: center;'>Monthly Timeline</h1>", unsafe_allow_html=True)
        monthly_stats_df = analysis.monthly_stats(selected_user, df)

        fig, ax = plt.subplots(figsize=(5,3))
        ax.plot(monthly_stats_df['month_year'], monthly_stats_df['message'], color = 'darkcyan')
        plt.xticks(rotation='vertical')
        plt.xlabel('Month')
        plt.ylabel('Messages')
        st.pyplot(fig)

        # DAILY TIMELINE 
        st.markdown("<h1 style='text-align: center;'>Daily Timeline</h1>", unsafe_allow_html=True)
        daily_stats_df = analysis.daily_stats(selected_user, df)

        fig, ax = plt.subplots(figsize=(5,3))
        ax.plot(daily_stats_df['only_date'], daily_stats_df['message'], color = 'darkcyan')
        plt.xticks(rotation='vertical')
        plt.ylabel('Messages')
        st.pyplot(fig)

        # TOP DAYS 
        st.markdown("<h1 style='text-align: center;'>Most Active Days</h1>", unsafe_allow_html=True)
        activity_day = analysis.top_days(selected_user, df)
        
        fig,ax = plt.subplots()
        bars = ax.barh(activity_day.index, activity_day.values, color = 'steelblue')
        ax.bar_label(bars, label_type='center')
        plt.xticks(rotation='vertical')
        plt.xlabel('Messages')
        plt.ylabel('Day')
        st.pyplot(fig)

        # TOP WORDS SECTION
        st.markdown("<h1 style='text-align: center;'>Most Used Words</h1>", unsafe_allow_html=True)
        top_words_df = analysis.top_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(top_words_df[0], top_words_df[1], color='steelblue')
        plt.xticks(rotation='vertical')
        plt.xlabel('Words')
        plt.ylabel('Count')
        st.pyplot(fig)

        # TOP EMOJIS SECTION
        st.markdown("<h1 style='text-align: center;'>Most Used Emojis</h1>", unsafe_allow_html=True)
        top_emojis_df = analysis.top_emojis(selected_user, df)

        col1, col2, col3 = st.columns([1,2,1])  # for centering the dataframe
        with col1:
            st.title('')
        with col2:
            st.dataframe(top_emojis_df)
        with col3:
            st.title('')

        # WORDCLOUD SECTION
        st.markdown("<h1 style='text-align: center;'>Word Cloud</h1>", unsafe_allow_html=True)
        df_wc = analysis.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        plt.axis("off")
        st.pyplot(fig)

        

        
        
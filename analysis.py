import re
import pandas as pd
import numpy as np
from wordcloud import WordCloud    
from collections import Counter
import emoji

# preprocessing the dataframe
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M - ')

    users = []
    messages=[]
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Chat notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns = ['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    return df

# fetching chat history
def fetch_chat(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df

# fetching total stats
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # no. of messages  
    num_mess = df.shape[0]  

    # no. of words
    words=[]
    for message in df['message']:
        words.extend(message.split())  

    # no. of media messages
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    # deleted messages
    temp1 = df[df['message'] == 'This message was deleted\n'].shape[0]
    temp2 = df[df['message'] == 'You deleted this message\n'].shape[0]
    num_deleted = temp1 + temp2
    return num_mess, len(words), num_media, num_deleted

# getting unique users and adding a overall option
def unique_users(df):
    user_list = df['user'].unique().tolist()
    if 'Chat notification' in user_list:
        user_list.remove('Chat notification')   
        
    user_list.sort()
    user_list.insert(0,'Overall')

    return user_list


# top message senders
def top_users(df):
    temp = df[df['user'] != 'Chat notification']
    x = temp['user'].value_counts().head()
    temp = round((temp['user'].value_counts()/temp.shape[0])*100, 2).reset_index().rename(columns={'index':'name','user':'percent'})
    temp.index = np.arange(1, len(temp) + 1)

    return x, temp.transpose()

# word cloud 
def create_wordcloud(selected_user, df):
    alphabets = open('alphabets.txt').read()
    temp = df[df['message'] != '<Media omitted>\n']

    if selected_user != 'Overall':
        temp = temp[temp['user'] == selected_user]

    wc = WordCloud(width=500, height=350, min_font_size=10, background_color='white')
    
    # removing single letter words
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if(word not in alphabets):
                words.append(word)

    msg = ' '.join(words)
    df_wc = wc.generate(msg)

    return df_wc

# most used words
def top_words(selected_user, df):
    stop_words = open('stop_hinglish.txt').read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
    temp = temp[temp['message'] != 'You deleted this message\n']
    temp = temp[temp['user'] != 'Chat notification']

    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if((word not in stop_words) and (word[0] != '@')):
                words.append(word)

    top_words_df= pd.DataFrame(Counter(words).most_common(15))
    return top_words_df

# most used emojis
def top_emojis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        for word in message.split():
            if emoji.is_emoji(word):
                emojis.append(word)
    
    top_emoijs_df = pd.DataFrame(Counter(emojis).most_common(10)).transpose()
    top_emoijs_df.rename(index={0:'emoji', 1:'count'}, inplace=True)
    top_emoijs_df.columns = np.arange(1, top_emoijs_df.shape[1]+1)
    
    return top_emoijs_df

# message stats by month
def monthly_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    monthly_stats_df = df.groupby(['year','month_num', 'month']).count()['message'].reset_index()
    month_year = []
    for i in range(monthly_stats_df.shape[0]):
        month_year.append(str(monthly_stats_df['month'][i])[0:3] + '-' + str(monthly_stats_df['year'][i])[2:4])

    monthly_stats_df['month_year'] = month_year

    return monthly_stats_df

# message stats by day
def daily_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_stats_df = df.groupby('only_date').count()['message'].reset_index()
    return daily_stats_df

# activity by day
def top_days(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()
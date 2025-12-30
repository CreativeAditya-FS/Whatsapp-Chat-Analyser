import re
import pandas as pd

def preprocess(data):

    # Supports:
    # [20/12/25, 3:46:30 PM] Name:
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s?[APap][Mm]\]'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    if len(messages) == 0:
        return pd.DataFrame(columns=['user', 'message'])

    df = pd.DataFrame({
        'user_message': messages,
        'message_date': dates
    })

    df['message_date'] = (
        df['message_date']
        .str.replace('[', '', regex=False)
        .str.replace(']', '', regex=False)
    )

    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='mixed',
        dayfirst=True
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    msgs = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if entry[1:]:
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append('group_notification')
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs
    df.drop(columns=['user_message'], inplace=True)

    # -------------------- DATE FEATURES --------------------
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour

    df['period'] = df['hour'].apply(
        lambda x: '23-00' if x == 23 else f'{x:02d}-{(x+1)%24:02d}'
    )

    return df
"""
Mit diesem Script werden Tweets aus einer Tabelle ausgelesen und 
die einzelnen Wörter in den Tweets gezählt
"""

import pandas as pd
from collections import Counter
import pyprind
from string import punctuation
import numpy as np
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqldb://root:@localhost:3306/coindata?charset=utf8', echo=False, convert_unicode=True, encoding= 'utf8')
df= pd.read_sql_table('tweets', engine)
tweets_text=df[df.columns[0]].copy()

#TestCode
#data= np.array(['a', 'b', 'a', 'a', 'b'])
#df= pd.DataFrame(data=data, columns=['tweet_text'])

counts= Counter()
pbar=pyprind.ProgBar(len(df['tweet_text']),
                     title='Vorkommen der Wörter zählen')

for i, t in enumerate(df['tweet_text']):
    text= ''.join([c if c not in punctuation else ' \
                '+c+' ' for c in t]).lower()
    df.loc[i, 'tweet_text']= text
    pbar.update()
    counts.update(text.split())



word_counts=sorted(counts, key=counts.get, reverse=True)

word_to_int= {word: ii for ii, word in
              enumerate(word_counts,1)}

mapped_tweets =[]
pbar= pyprind.ProgBar(len(df['tweet_text']))

for tweet in df['tweet_text']:
    mapped_tweets.append([word_to_int[word] for word in tweet.split()])


print()
print('words and counts: ', counts)
print('distinct words: ', word_counts[:])
print('tweets as word indices: ',mapped_tweets)
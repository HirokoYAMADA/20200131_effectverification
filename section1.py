#%%
import requests
import io
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

url = 'http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv'
res = requests.get(url).content
df: pd.DataFrame = pd.read_csv(io.StringIO(res.decode('utf-8')), header=0)

#%%
df
#%%
df.dtypes
# %%
df.describe().round(2)
# %%
df.groupby('recency').count().visit
# %%
df.groupby('recency').count().visit.plot.bar()
# %%
df.groupby(['womens', 'mens']).count().visit
# %%
df.groupby('history_segment').count().visit
# %%
df.groupby('history_segment').count().visit.plot.bar()
# %%
df.groupby('channel').count().visit

#%%
df.corr()
  
# %%　まず男性向けメールが配信されたサンプルとメールが配信されなかったサンプルにデータを限定するため、女性向けメールが配信されたデータを削除。
df2: pd.DataFrame = df[df.segment != 'Womens E-Mail']
df2.groupby('segment').count().visit
# %%
df2['treatment'] = np.where(df2['segment'] == 'Mens E-Mail', 1, 0)
df2.groupby('treatment').mean()[['conversion', 'spend']]
# %%
df_mens = df2[df2['treatment']==1]
df_nomail = df2[df2['treatment']==0]

# %%
df_mens.describe()
# %%
df_nomail.describe()
# %%
#上記の結果には一見差があるように見えるが、実際あるのだろうか？
#上記の結果はRCTの結果得られており、セレクションバイアスの問題は考慮しなくてよいため、検定で有意差が認められれば効果があったと言/うことができる.
#検定手法を選ぶためには観測値が正規分布に従っているかと2つの郡で分散が等しいかをまず検定してやる必要がある。
# %%
t, p = stats.ttest_ind(df_mens.spend, df_nomail.spend, equal_var=True)
print('p-value =', p)

# %%
#次にバイアスがある場合について検証する
# %%
   



# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 20:42:37 2022

@author: 陈纪程
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sb

avalible_files = ['voyage-to-the-sunken-city','forged-in-the-barrens','ashes-of-outland','rise-of-shadows',\
                  'the-witchwood','fractured-in-alterac-valley','united-in-stormwind','madness-at-the-darkmoon-faire',\
                      'scholomance-academy','descent-of-dragons','saviors-of-uldum']

i = 0
change = pd.DataFrame(index=[],columns=['cost_mean','relative','P_value'])
change.index.name = 'file_name'
df_total = pd.DataFrame(columns=['cost','CE','HP','CP'])
dfT_test = pd.DataFrame(columns=['test_N'])
Judge = []
for file_name in avalible_files:
    i += 1
    df = pd.read_csv("D://heartstone/{0}/{1}.csv".format(file_name,file_name),encoding='utf-8')
    cost_mean = float(df[['cost']].mean())
    df_num = df[['cost','CE','HP']]

    for x in df.index:
        if pd.isnull(df_num.loc[x,'CE']):
            df_num.drop(x,inplace = True)
    
    for_test = pd.DataFrame()
    for_test['test_N'] = df_num['CE'].map(int) + df_num['HP'].map(int) - 2 * df_num['cost'].map(int)
    n = int(for_test['test_N'].count())
    t_test = float(for_test['test_N'].mean())*pow(n,0.5)/float(for_test['test_N'].var())
    judgement = 'in {0} 2*cost == HP + CE is {1}'.format(file_name,abs(t_test) < stats.t.isf(0.025,n-1))
    Judge.append(judgement)
    
    df_num['CP'] = (df_num['CE'].map(int) + df_num['HP'].map(int)) / 2
    dfT_test = pd.concat([dfT_test,for_test], ignore_index = True)
    df_total = pd.concat([df_total,df_num], ignore_index = True)
    
    r,p_value = stats.pearsonr(df_num['CP'],df_num['cost'])#计算CP和cost之间的相关系数和对应的显著性
    change.loc[file_name] = [cost_mean,r,p_value]

    r_pearson = df_num.corr()
    fig = plt.figure(i)
    sb.heatmap(data = r_pearson,cmap="YlGnBu")
    plt.savefig("D://heartstone/{0}/{1}.png".format(file_name,i),bbox_inches = 'tight')
    plt.close()

r_pearson = df_total.corr()
fig = plt.figure(1)
sb.heatmap(data = r_pearson)
plt.savefig("D://heartstone/total_relatives.png",bbox_inches = 'tight')

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
df_total2 = pd.DataFrame(df_total['cost'].value_counts(),columns=['cost'])
df_total2.rename(columns={'cost':'frequency'},inplace=True)
df_total2.index.name='cost'
df_total2.reset_index(drop=False,inplace=True)
df_total2.plot(x='cost',y='frequency',kind='barh',ax=ax)
plt.savefig("D://heartstone/total_distrubution.png")

change.reset_index(drop=False,inplace=True)
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
change.plot(x='file_name',y=['cost_mean','relative','P_value'],ax=ax,legend=True,marker='o',color=['r','g','b'])
plt.xticks(rotation=60)
plt.tight_layout()
plt.show()
plt.savefig("D://heartstone/total_change.png")

n = int(dfT_test['test_N'].count())
t_test = float(dfT_test['test_N'].mean())*pow(n,0.5)/float(dfT_test['test_N'].var())
final = 'Generally,2*cost == HP + CE is {0}'.format(abs(t_test) < stats.t.isf(0.025,n-1))
Judge.append(final)
for Judgement in Judge:
    print(Judgement)
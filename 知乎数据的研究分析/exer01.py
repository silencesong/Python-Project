import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']#显示中文

# 数据读取
data1=pd.read_csv("G:/mystudy/study/exercise/知乎/知乎数据_201701.csv",engine="python")
data2=pd.read_csv("G:/mystudy/study/exercise/知乎/六普常住人口数.csv",engine="python")
# print(data1.head())
# print(data2.head())

# 数据清洗—去除空值
# 文本型字段空值为"缺失数据"，数字型字段空值改为0
# 提示:fillna方法填充缺失数据，注意insplce参数,该函数可以将任意数据内空值替换
def data_cleaning(df):
    cols=df.columns
    for col in cols:
        if df[col].dtype=="object":
            df[col].fillna("缺失数据",inplace=True)
        else:
            df[col].fillna(0,inplace=True)
    return df
data1_c=data_cleaning(data1)
# print(data1_c.head(10))


# 问题1 知友全国地域分布情况，分析出TOP20
# 要求：
# ① 按照地域统计 知友数量、知友密度（知友数量/城市常住人口），不要求创建函数
# ② 知友数量，知友密度，标准化处理，取值0-100，要求创建函数
# ③ 通过多系列柱状图，做图表可视化
# 提示：
# ① 标准化计算方法 = (X - Xmin) / (Xmax - Xmin)
# ② 可自行设置图表风格
df_city=data1_c.groupby('居住地').count()# 按照居住地统计知友数量
data2['city']=data2['地区'].str[:-1]# 城市信息清洗，去掉城市等级文字
# print(df_city.head())
# print(data2.head())


# 统计计算知友数量，知友密度
qldata=pd.merge(df_city,data2,left_index=True,right_on="city",how="inner")[['_id','city','常住人口']]
qldata['知友密度']=qldata['_id']/qldata['常住人口']
# print(qldata.head())

# 创建函数，结果返回标准化取值，新列列名
def data_nor(df,*cols):
    colnames=[]
    for col in cols:
        colname=col+'_nor'
        df[colname]=(df[col]-df[col].min())/(df[col].max()-df[col].min())*100
        colnames.append(colname)
    return (df,colnames)

# 标准化取值后得到知友数量，知友密度的TOP20数据
resultdata=data_nor(qldata,'_id','知友密度',)[0]
resultcolnames=data_nor(qldata,'_id','知友密度',)[1]
# print(resultdata)
# print(resultcolnames)#['_id_nor', '知友密度_nor']

qldata_top20_sl=resultdata.sort_values(resultcolnames[0],ascending=False)[['city',resultcolnames[0]]].iloc[:20]
qldata_top20_md=resultdata.sort_values(resultcolnames[1],ascending=False)[['city',resultcolnames[1]]].iloc[:20]
# print(qldata_top20_sl)
# print(qldata_top20_md)

# 创建图表
fig1=plt.figure(num=1,figsize=(12,4))
y1=qldata_top20_sl[resultcolnames[0]]
plt.bar(range(20),y1,width=0.8,facecolor="yellowgreen",edgecolor="k",tick_label=qldata_top20_sl['city'])
plt.title("知友数量T20\n")
plt.grid(True,linestyle='--',color='gray',linewidth='0.5',axis='y')
for i,j in zip(range(20),y1):
    plt.text(i+0.1,2,'%.f'%j,color='k',fontsize=9)

fig2=plt.figure(num=2,figsize=(12,4))
y2=qldata_top20_md[resultcolnames[1]]
plt.bar(range(20),y2,width=0.8,facecolor="lightskyblue",edgecolor="k",tick_label=qldata_top20_md['city'])
plt.title("知友密度T20\n")
plt.grid(True,linestyle='--',color='gray',linewidth='0.5',axis='y')
for i,j in zip(range(20),y2):
    plt.text(i,2,'%.2f'%j,color='k',fontsize=9)
# plt.show()


# 问题2 不同高校知友关注和被关注情况
# 要求：
# ① 按照学校（教育经历字段） 统计粉丝数（‘关注者’）、关注人数（‘关注’），并筛选出粉丝数TOP20的学校，不要求创建函数
# ② 通过散点图 → 横坐标为关注人数，纵坐标为粉丝数，做图表可视化
# ③ 散点图中，标记出平均关注人数（x参考线），平均粉丝数（y参考线）
# 提示：① 可自行设置图表风格

# 统计计算学校的粉丝数、被关注量
q2data=data1_c.groupby("教育经历").sum()[['关注','关注者']].drop(['缺失数据','大学','本科'])
# print(q2data)
q2data_c=q2data.sort_values('关注',ascending=False)[:20]
# print(q2data_c)

plt.figure(figsize=(10,6))
x=q2data_c['关注']
y=q2data_c['关注者']
follow_mean=q2data_c['关注'].mean()
fans_mean=q2data_c['关注者'].mean()
# 创建散点图
plt.scatter(x,y,marker="o",c="b",s=y/1000,cmap="Blues",alpha=0.8,label='学校')
plt.xlabel("关注人数",fontsize=16)
plt.ylabel("粉丝数",fontsize=16)
# 添加显示内容
plt.axvline(follow_mean,label="平均关注人数：%d人" % follow_mean,color='r',linestyle="--",alpha=0.8) #添加x轴参考线
plt.axhline(fans_mean,label="平均粉丝数：%d人" % fans_mean,color='g',linestyle="--",alpha=0.8) #添加y轴参考线
plt.legend(loc="upper left")
plt.grid()
# 添加注释
for i,j,n in zip(x,y,q2data_c.index):
    plt.text(i+500,j,n,color="k")

plt.show()

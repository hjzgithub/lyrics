# -*- coding: utf-8 -*-

'''
import requests
from bs4 import BeautifulSoup
import re
import json
import csv

# 获取周杰伦十四张专辑所有歌歌词与评论数,并存储到csv
album_urls = {'Jay 同名专辑': 'https://music.163.com/album?id=18918',
              '范特西': 'https://music.163.com/album?id=18915',
              '八度空间': 'https://music.163.com/album?id=18907',
              '叶惠美': 'https://music.163.com/album?id=18905',
              '七里香': 'https://music.163.com/album?id=18903',
              '十一月的萧邦': 'https://music.163.com/album?id=18896',
              '依然范特西': 'https://music.163.com/album?id=18893',
              '我很忙': 'https://music.163.com/album?id=18886',
              '魔杰座': 'https://music.163.com/album?id=18877',
              '跨时代': 'https://music.163.com/album?id=18875',
              '惊叹号': 'https://music.163.com/album?id=18869',
              '十二新作': 'https://music.163.com/album?id=2263029',
              '哎呦,不错哦': 'https://music.163.com/album?id=3084335',
              '周杰伦的床边故事': 'https://music.163.com/album?id=34720827'}

album_urls2 = {'Jay':'https://y.qq.com/n/yqq/album/000f01724fd7TH.html',
               '范特西':'https://y.qq.com/n/yqq/album/000I5jJB3blWeN.html',
               '八度空间':'https://y.qq.com/n/yqq/album/004MGitN0zEHpb.html',
               '叶惠美':'https://y.qq.com/n/yqq/album/000MkMni19ClKG.html',
               '七里香':'https://y.qq.com/n/yqq/album/003DFRzD192KKD.html',
               '十一月的萧邦':'https://y.qq.com/n/yqq/album/0024bjiL2aocxT.html',
               '依然范特西':'https://y.qq.com/n/yqq/album/002jLGWe16Tf1H.html',
               '我很忙':'https://y.qq.com/n/yqq/album/002eFUFm2XYZ7z.html',
               '魔杰座':'https://y.qq.com/n/yqq/album/002Neh8l0uciQZ.html',
               '跨时代':'https://y.qq.com/n/yqq/album/000bviBl4FjTpO.html',
               '惊叹号':'https://y.qq.com/n/yqq/album/003KNcyk0t3mwg.html',
               '十二新作':'https://y.qq.com/n/yqq/album/003Ow85E3pnoqi.html',
               '哎呦，不错哦':'https://y.qq.com/n/yqq/album/001uqejs3d6EID.html',
               '周杰伦的床边故事':'https://y.qq.com/n/yqq/album/003RMaRI1iFoYd.html'}

# 网易云歌词爬取
def get_songs_by_albums(album_urls):
    
    #专辑网址->歌曲名称+歌曲id
    # 遍历所有专辑
    song_ids = {}
    for album_title, album_url in album_urls.items():
        
        # 爬取并解析网页
        r = requests.get(album_url, headers =
                         {'User-Agent': 'Mozilla/5.0',
                          'Referer': 'http://music.163.com/',
                          'Host': 'music.163.com'})
        demo = r.text
        soup = BeautifulSoup(demo, 'lxml')
        
        # 结合正则表达式抓取歌曲id
        for meta in soup.find_all('meta', {'property': "og:music:album:song"}):
            content = meta.attrs['content']
            title, url = re.match(r'title=(.*);url=(.*)',content).group(1,2)
            regex = re.compile(r'id=(.*)')
            song_id = regex.findall(url)[0]
            song_ids[title] = song_id
            
    return song_ids

def get_lyrics_by_songs(song_ids):
    song_lrcs = {}
    for song_title, song_id in song_ids.items():
        song_url = 'http://music.163.com/api/song/lyric?id=' + str(song_id) + '&lv=1&kv=1&tv=-1'
        
        # 爬取并解析页面
        r = requests.get(song_url, headers= {'User-Agent': 'Mozilla/5.0',
                          'Referer': 'http://music.163.com/',
                          'Host': 'music.163.com'})
        demo = r.text
        lrc_json = json.loads(demo)
        
        # 抓取歌词
        lrc = lrc_json['lrc']['lyric']
        pat = re.compile(r'\[.*\]') # 去掉歌词的时间标注
        lrc = re.sub(pat, "", lrc)
        lrc = lrc.strip()
        song_lrcs[song_title] = lrc
    
    return song_lrcs

# 网易云音乐评论数爬取
def get_comments_by_songs(song_ids):
    
    comments_total = {}

    for song_title, song_id in song_ids.items():
        song_url = 'http://musicapi.leanapp.cn/comment/music?id=' +str(song_id) + '&limit=1'
        
        # 爬取并解析页面
        r = requests.get(song_url, headers =
                         {'User-Agent': 'Mozilla/5.0',
                          'Referer': 'http://musicapi.leanapp.cn',
                          'Host': 'musicapi.leanapp.cn'})
        demo = r.text
        total_json = json.loads(demo)
        
        # 抓取评论数
        total = total_json['total']
        comments_total[song_title] = total
        
    return comments_total

# QQ音乐评论数爬取
def get_songids_by_album_urls(album_urls):
    song_ids = {}
    for album_title, album_url in album_urls.items():
        
        # 爬取并解析网页
        r = requests.get(album_url, headers =
                         {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                          'Referer': 'https://y.qq.com/n/yqq/song/0039MnYb0qxYhV.html',
                          'Host': 'y.qq.com'})
        demo = r.text
        mid = re.findall(r'\smid="(.*)"', demo)
        title1 = re.findall(r'html"\stitle="(.*?)"', demo)
        title = title1.copy()
        allsongs = []
        for i in title:
            if i != '周杰伦' and i != '潘儿' and i != 'Lara梁心颐' and i!='林迈可' and i!='费玉清' and i!= '杨瑞代' and i!= '袁咏琳':
                allsongs.append(i)
        for i in range(len(allsongs)):
            song_ids[allsongs[i]] = mid[i]
        
    return song_ids

def get_comments_by_song_ids(song_ids):
    comments_total_qq = {}
    for song_title, song_id in song_ids.items():
        song_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?g_tk_new_20200303=5381&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=GB2312&notice=0&platform=yqq.json&needNewCode=0&cid=205360772&reqtype=1&biztype=1&topid=' + str(song_id) + '&cmd=4&needmusiccrit=0&pagenum=0&pagesize=0&lasthotcommentid=&domain=qq.com'
                    
        # 爬取并解析页面
        r = requests.get(song_url, headers =
                             {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                              'Referer': 'https://y.qq.com/n/yqq/song/0039MnYb0qxYhV.html',
                              'Host': 'y.qq.com'})
        demo = r.text
        total_json = json.loads(demo)
        # 抓取评论数
        total = total_json['commenttotal']
        comments_total_qq[song_title] = total
    return comments_total_qq   

# 写入csv    
def write_csv():
    song_ids = get_songs_by_albums(album_urls)
    all_lyrics = get_lyrics_by_songs(song_ids)
    comments_total = get_comments_by_songs(song_ids)
    comments_total_qq = get_comments_by_song_ids(get_songids_by_album_urls(album_urls2))
    
    file = open('U201816176.csv','w',encoding = 'utf-8',newline='')
    filewriter = csv.writer(file)
    
    filewriter.writerow([all_lyrics])
    filewriter.writerow([comments_total])
    filewriter.writerow([comments_total_qq])
    file.close()

write_csv()
'''














import csv
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud

# 读取csv
with open('U201816176.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    result = list(reader)
    
    songs_dict = eval(result[0][0])
    comments_dict = eval(result[1][0])
    comments = eval(result[2][0])

# 歌词内容与网易云音乐评论数
songs_name = list(songs_dict)
songs_content = [songs_dict[i] for i in songs_name]
songs_comments_total = [comments_dict[i] for i in songs_name]

# QQ音乐评论数的缺失值与歌名的异常值处理
    
names_qq = list(comments.keys())
comments_qq =  [comments[i] for i in names_qq]

names_qq1 = names_qq.copy()
for i in range(len(names_qq1)):
    if names_qq1[i] == '爸，我回来了':
        names_qq[i] = '爸我回来了'
    if names_qq1[i] == '免费教学录影带':
        names_qq[i] = '免费教学录像带'
    if names_qq1[i] == '我落泪情绪零碎':
        names_qq[i] = '我落泪 情绪零碎'
    if names_qq1[i] == '不该 (with aMEI)':
        names_qq[i] = '不该(with aMEI)'
    
lost = {'双刀': 3305,'飘移': 6769,'一路向北': 30362,'稻香': 37317,'超人不会飞': 8112,'超跑女神': 2712,'哪里都是你': 3530,'乌克丽丽': 2395,'美人鱼': 4414,'听见下雨的声音': 5223}

for i in songs_name:
    if i not in names_qq:
        n = songs_name.index(i)
        names_qq.insert(n, i)
        j = lost[i]
        comments_qq.insert(n, j)
        
# 作词人缺失值的处理
songs_lyrictists = []
lost = [] # 用来存储缺失值索引
for i in songs_content:
    lyrictist = re.findall(r'作词\s:\s(.*?)\n', i)
    if lyrictist:
        for j in lyrictist:
            songs_lyrictists.append(j)
    else:
        songs_lyrictists.append('')
        lost.append(songs_content.index(i)) # 根据值找到索引，由于值（歌名）是唯一的，所以可以这样处理


#for i in lost:
#   print(songs_name[i])

# 在网上找到所缺数据并填充，对不起：方文山，七里香：方文山，止战之殇：方文山，稻香：周杰伦
for i in lost[:3]:
    songs_lyrictists[i] = '方文山'
songs_lyrictists[lost[-1]] = '周杰伦'     
   
     
df1 = pd.DataFrame()
df1['歌名'] = songs_name
df1['作词人'] = songs_lyrictists
df1['歌词内容'] = songs_content
df1['网易云音乐评论数'] = songs_comments_total
df1['网易云音乐评论数'] = df1['网易云音乐评论数'].astype(object)
df1['QQ音乐评论数'] = comments_qq
df1['QQ音乐评论数'] = df1['QQ音乐评论数'].astype(object)
print(df1)


# 作词人分布情况
# 分组与聚合
def group_df(df):
    grouped = df.groupby(by='作词人')
    group_count = grouped['作词人'].count()
    return group_count

# print(group_df(df1))

# 可以发现有几个作词人实质是同一个人，进行修改
df2 = df1.copy()

for i in df2.index:
    if df2.loc[i, '作词人'] == '古小力/黄淩嘉':
        df2.loc[i, '作词人'] = '古小力/黄凌嘉'
    if df2.loc[i, '作词人'] == '宋健彰':
        df2.loc[i, '作词人'] = '宋健彰(弹头)'

# print(group_df(df2))
        
# 排序
df2_sort = group_df(df2).sort_values()

plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
plt.rcParams['figure.figsize'] = [12, 12] # 用来控制图片大小

person = []
number = []
for index in df2_sort.index:
    person.append(index)
    number.append(df2_sort[index])

# 转化为条形图
length = len(person)

def bar():
    plt.barh(range(length), number, height = 0.7, color = 'steelblue', alpha=0.8)
    plt.yticks(range(length), person)
    plt.xlim(0, 100)
    plt.xlabel('次数')
    plt.title('不同词作人作词次数')
    for x, y in enumerate(number):
        plt.text(y+0.2, x-0.1, '%s'% y)
    plt.savefig('作词人-条形图.jpg')
    plt.show()

# 转化为扇形图并突出显示占比最大者
def sector():
    explode = [0]*(length-1) + [0.1]
    
    fig, ax1 = plt.subplots()
    ax1.pie(number, explode=explode, labels=person, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.savefig('作词人-扇形图1.jpg')
    plt.show()

# 把低于5次的都归为其他,由于数据升序排列，故切片即可
for i in number:
    if i >= 5:
        cut = number.index(i) - 1
        break

person_cut = ['其他']
number_cut = np.sum(number[:cut])

# 拼接列表
number_copy = number.copy()
person_new = person[cut+1:] + person_cut
number_new = number_copy[cut+1:]
number_new.append(number_cut)

def sector2():        
    fig, ax1 = plt.subplots()
    ax1.pie(number_new, labels=person_new, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.savefig('作词人-扇形图2.jpg')
    plt.show()

bar()
sector()
sector2()

  
# 歌词内容的清洗（删掉与歌词无关的内容，即换行符到下一个换行符之间的匹配，并且剔除掉有冒号的以及一些多余字符）
df3 = df2.copy()
content_clean = df3['歌词内容']

a = []
for index in content_clean.index:
    i = content_clean[index]
    b = re.findall(r'\n(.*)', i)
    c = b.copy()
    for j in b:
        if ':' in j:
            c.remove(j)
        elif '：' in j:
            c.remove(j)
        elif 'ISRC' in j:
            c.remove(j)
        elif 'TWK' in j:
            c.remove(j)
        elif '《' in j:
            c.remove(j)
    a.append(c)

# 合并到df3
for index in range(len(a)):
    i = a[index]
    b = ''
    for j in i:
        pattern = re.compile(r'\t|\n| |？|：|（|）|(|)|~|、|\.|-|:|;|\)|\(|\?|"') # 定义正则表达式的匹配模式
        j = re.sub(pattern, '', j)
        if j:
            b += j
    a[index] = b

df3['歌词内容'] = a

# 分组，生成词云图
names = ['方文山', '周杰伦', '黄俊郎', '徐若瑄']

df4 = df3.copy()

def count(name):
    words = []
    numbers = []
    for i in df4.index:
        
        if df4.loc[i, '作词人'] == name:
            
            # 结巴分词
            j = df4.loc[i, '歌词内容']
            seg_list = jieba.cut(j, cut_all=False)
            
            # 去除停用词
            remove_words = ['的', '我','你', '在', '了', '是', '不','着','说','都','啦','让','就','有','那','却','谁','这','很','也','还','对','会','再','被','上','去','他','人','像','看','给','她'] 
            result_list = []
            for word in seg_list:
                if word not in remove_words:
                    result_list.append(word)
            df4.loc[i, '歌词内容'] = result_list
            
            # 词频统计
            k = pd.Series(result_list)
            
            for index in k.index:
                words.append(index)
                numbers.append(k[index])          
    s = [words, numbers] 
    return s

# 词云展示结果
def show():
    for name in names:
        c = count(name)
        d = c[1]
        count_result = pd.Series(d).value_counts().sort_values(ascending=False)
        count_result1 = count_result.head(10)
        print(name+'常用词：')
        print(count_result1)
        print(name+'画像：')
        
        # 定义词云图
        wc = WordCloud(
                width = 1600,
                height = 900,
                background_color = 'white',
                mode = 'RGB',
                max_words = 600,
                font_path = r'C:\Windows\Font\simkai.ttf',
                max_font_size = 150,
                relative_scaling = 0.6,
                random_state = 50,
                scale = 2
                ).generate(' '.join(d))
        
        # 产生词云
        wc.generate(' '.join(d))
        
        plt.imshow(wc, interpolation = 'bilinear')
        plt.axis('off')
        plt.show()
        
        wc.to_file(name +'词云.jpg') 

show()
        

# 生成折线图
x = list(range(150))
y = songs_comments_total
y2 = comments_qq

plt.plot(x,y,color='red',label='网易云音乐',linewidth=1.0)
plt.plot(x,y2,color='yellow',label='QQ音乐',linewidth=2.0)

plt.title('歌曲评论数')
plt.savefig('歌曲评论数1.jpg')
plt.show()

# 找到异常值，返回索引
for i in x:
    if y[i] > 250000:
        print(df4.loc[i,'歌名'])
        print(i)
        
def de(l):        
    l_copy = l.copy()
    l_copy.pop(32)
    l_copy.pop(146)
    return l_copy

x_copy = de(x)
y_copy = de(y)
y2_copy = de(y2)

plt.plot(x_copy,y_copy,color='red',label='网易云音乐',linewidth=1.0)
plt.plot(x_copy,y2_copy,color='yellow',label='QQ音乐',linewidth=2.0)

plt.title('歌曲评论数')
plt.savefig('歌曲评论数2.jpg')
plt.show()

# 回归模型
y_wy = np.array(y_copy)
y_qq = np.array(y2_copy)

def reg(x,y,i):
    
    a = x - np.mean(x)
    b = y - np.mean(y)
    c = (sum(a**2))**(0.5)
    d = (sum(b**2))**(0.5)

    if i < 1:
        print('QQ音乐评论数对网易云音乐评论数回归：')
    else:
        print('异方差检验：')
        
    r = sum(a*b)/(c*d)
    print('相关系数：',r)
    
    b1 = sum(a*b)/sum(a**2)
    b0 = np.mean(y)-b1*np.mean(x)
    
    print('回归模型：','y','=',b0,'+',b1,'*','x')
    
    y_hat = b0 + b1*x 
    e = y- y_hat

    # 拟合优度
    R_2 = 1 - sum(e**2)/sum(b**2)
    print('拟合优度：',R_2)
    
    # 双变量回归的系数的显著性：t检验
    n = len(x)
    se = ((sum(e**2)/(n-2))/(n*sum(a**2)/(n-1)))**(0.5)
    t1 = b1/se
    print('b1的t值：',t1)
    
    # 异方差检验
    if i < 1:
        # 稳健标准误
        se_c = (sum(e**2*a**2)/((sum(a**2))**2))**(0.5)
        t1_c = b1/se_c
        print('b1的t值（稳健）：',t1_c)
        
        # 拟合曲线与残差图
        ax1 = plt.subplot(2,1,1)
        ax2 = plt.subplot(2,1,2)
        
        plt.sca(ax1)
        plt.scatter(x,y)
        plt.plot(x,y_hat,color='g')
        plt.title('散点图与拟合曲线图')
        plt.xlabel('QQ音乐评论数')
        plt.ylabel('网易云音乐评论数')
        
        plt.sca(ax2)
        plt.scatter(x,e)
        plt.title('残差图')
        plt.savefig('回归.jpg')
        plt.show()
        
        reg(y_hat,e**2,1)
    
reg(y_qq,y_wy,0)





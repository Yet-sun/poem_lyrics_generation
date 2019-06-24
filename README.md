# poem_lyrics_generation

LSTM语言模型古诗生成，歌词生词，数据处理，网站

## 一、主要文件说明

- poem_app：Django组件

- poem_backend：Django设置及路由配置

- static：静态资源

- templates：前端html文件

- chinese_poem_generate：基于lstm模型的诗歌生成模型训练及验证

- lyrics_generation：基于lstm模型的诗歌生成模型训练及验证

- data_crawl: 数据爬取文件

- data_processing：输出处理文件

- lstm_model：基于lstm的概率语言模型进行歌词生成，train_lstm_word_based.py是训练代码，generateLyrics_word_based.py是生成代码

- train_data：训练数据

## 二、使用说明

### 1、训练数据

```
# lstm模型训练（古诗生成）
> cd ...chinese_poem_generate
> python train.py

# lstm模型训练（歌词生成）
> cd ...lstm_model
> python train_lstm_word_based.py
```

### 2、生成歌词
```
# lstm模型生成歌词
> cd ...chinese_poem_generate
> python eval_poem.py

# lstm模型生成歌词
> cd ...lstm_mode
> python generateLyrics_word_based.py
```

## 三、详细说明

### 1、数据爬取
主要爬取网易云音乐网页（https://music.163.com） 的林俊杰的歌词数据。

具体的代码在data_crawl文件夹中。

### 2、数据处理

(1)古诗数据

生成词汇表，并将古诗转换为词向量，填充词向量并转化为np数组

(2)歌词数据

数据处理主要将数据爬取中的结果（多个歌曲文件）合并成一个文件，并去掉一些歌词生成的干扰信息，如歌手：林俊杰，作词：林俊杰等信息，另外，本任务是生成中文歌词，可以将一些英文歌词去掉。

### 3、生成

古诗和歌词生成均使用了基于lstm的概率语言模型：

#### 3.1 基于lstm的概率语言模型

（1）模型结构如下：

- 古诗：

使用了2层LSTM，后面接了一个softmax

- 歌词：

<div align=center><img src="https://github.com/Yet-sun/poem_lyrics_generation/tree/master/poem_backend/poem_app/lyrics_generation/lstm_model/lstm_structure.png" width="50%" alt="基于lstm的概率语言模型结构"/></div>

本模型使用了2层LSTM，一层全连接层，全连接层后面接了一个softmax，也就是分类模型。

（2）结果展示：

以“中国牛逼”开头

```
中国牛逼
不同太多
你最见你
不在
甜
如影
杀开了耳丽
苦结几的眼光
披天前的就会想
网碌水的步悉
越流泪的机场
身再友的跟底灯撑着学一个让爱的爱
愿是所有说说
只许你到我会好的
也许你在
数了脑海
握着时夜
我作头在
山车难难
你怎么好
当你看到
善变代表对你太感冒
要你听到
善变代表对你太感冒
要你听到
我有我最独特思考
要你看到
爱情不只华丽
外灯是是爱的尽
累与整气到熟
为你的为你在我
```

## 四、参考博客

https://blog.csdn.net/quiet_girl/article/details/84768821 

https://www.jb51.net/article/137118.htm

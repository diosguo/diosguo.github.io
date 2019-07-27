---
layout: post
title: '强化学习的句子选择及摘要'
subtitle: 'Fast Abstractive Summarization with Reinforce-Selected Sentence Rewriting'
date: 2019-07-27
categories: 文本摘要
author: Dardis
cover: '/assets/blog_img/2018_ACL_Fast_withReinforceSelectedSentenceRewrite.assets/timg.jpg'
tags: 文本摘要 论文解读 NLP
---


> Chen, Y. C. , & Bansal, M. . (2018). Fast abstractive summarization with reinforce-selected sentence rewriting.

发表：ACL 2018

PDF地址：[https://arxiv.org/pdf/1805.11080.pdf](https://arxiv.org/pdf/1805.11080.pdf)

代码地址:  [https://github.com/ChenRocks/fast_abs_rl](https://github.com/ChenRocks/fast_abs_rl)



## 1 概述

- 套路：首先进行句子选择，然后对每个选出来的句子进行摘要式的重写，并根据强化学习中的梯度策略，提出了一个新的方法来将句子选择与句子摘要两个网络连接起来。
- 数据集：CNN/DailyMail
- 优点：
  - 一定程度上减少了生成重复内容的情况
  - 由于选出不同句子进行摘要，便可以并行运算，速度快了很多



## 2 模型

### 2.1 句子抽取

论文模型如下图，大概看下结构就好，论文这个图感觉有点乱，请看下面描述：

![extractor]({{ "/assets/blog_img/2018_ACL_Fast_withReinforceSelectedSentenceRewrite.assets/1564126677273.png" | absolute_url}})

#### 2.1.1 生成句子语义表述

如果要对句子进行选择，那么需要句子对应的特征，此处论文中使用**时序的CNN**计算每个句子的表述向量$r_i$，然后按照一般套路，为了考虑上下文信息，加入了**双向LSTM**，得到更厉害的表述向量$h_i$。（CNN就是灰色部分，LSTM是蓝色部分。

#### 2.1.2 选择句子

有了强大的句子表述，我们就可以根据$h_i$算出来哪个句子是重要的，需要抽取出来。这里模型使用了一个传统的Decoder：**单向LSTM**再加上两层Attention计算每个句子被抽取出来的概率，这Attention的部分没画出来，且看我下面（嘿嘿）：

首先将$h_i$作为输入传入这个LSTM得到输出$z_i$，其中$c$是LSTM中的隐藏单元:

$$
z_i = LSTM(c,h_i)
$$

然后计算一层Attention，找到注意的句子：

$$
a_j^t=v_g^Ttanh(W_{g1}h_j+W_{g2}z_t)
$$

$$
\alpha^t=softmax(a^t)
$$

$$
e_t=\sum_j\alpha_j^tW_{g1}h_j
$$

再接一层Attention，就算出每个句子的概率：

$$
u_{j}^{t}=\left\{\begin{array}{ll}{v_{p}^{\top} \tanh \left(W_{p 1} h_{j}+W_{p 2} e_{t}\right)} & {\text { if } j_{t} \neq j_{k}} \\  & {\forall k<t} \\ {-\infty} & {\text { otherwise }}\end{array}\right.
$$

$$
P(j_t|j_1,\cdots,j_{t-1}) = softmax(u^t)
$$

这里就可以设置一个阈值，比如概率大于多少的，就是看抽取出来的句子。

### 2.2 对句子进行摘要

这个部分就比较简单了，使用一个普通的Attention Seq2Seq模型，再加上Pointer Generator来从原文复制词解决OOV问题，没啥好说的。



## 3 学习与训练

论文中提到，抽取句子的过程是一种硬性选择的过程，那么在抽取与摘要之间的这个过程是不可微分的，也就是不能反向传播误差，所以不能简单地训练。他就使用了一个RL中的梯度策略方法，来建立反向传播的连接。

而且，两个模型一开始学的都不准，然后他两放一起，大家都不准，还会影响对方。所以一开始对这两个模型分别训练，各自的效果有点好了，在用上面说的RL方法将两个模型放一起训练。

### 3.1 先解决数据问题

- 句子选择：
  - 现在大家伙用的数据集DUC，CNN/DM都没有句子选择的这种标签，也就是没有标出来哪个句子是要留下的，那么如何放在这个模型中训练呢？论文提出了一个简单的方法，先自己生成一个“**代理**”标签，他是这么计算来的：

$$
j_t = argmax_i(\text{ROUGE-L}_{recall}(d_i,s_t))
$$

​	其中$s_t$是真实摘要中第$t$个句子，这样就把原始摘要中的每个句子，都在原始文本中找到了一个句子与之对应，也就是打了**我要抽取这个句子**的标签。然后用这个标签去训练，妥妥的。

- 句子摘要
  - 这部分，就直接把上面句子选择部分求出来的摘要句子与对应的原始句子做训练数据就行。

### 3.2 强化学习

<h1>对不起了，老铁们，强化学习看不动啊，等我学完了我再更新哈</h1>

### 3.3 减少重复

在选择句子的时候，用Beam Size为$k$的Beam Search查找要找到句子们，然后对$k^n$个可能的组合按照其中出现重复N-gram的数量进行排序，重复的越少分数越高。另外还用了diverse decoding algorithm这个算法。



## 4 结果

![score]({{ "/assets/blog_img/2018_ACL_Fast_withReinforceSelectedSentenceRewrite.assets/1564132097380.png" | absolute_url }})

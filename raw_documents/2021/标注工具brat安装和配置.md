subtitle 标注工具Brat的安装和配置

categories 感悟

cover ![](%E6%A0%87%E6%B3%A8%E5%B7%A5%E5%85%B7brat%E5%AE%89%E8%A3%85%E5%92%8C%E9%85%8D%E7%BD%AE.assets/1.jpg)

tags 工具 NLP

brat是一个基于web的NLP文本标注工具，支持关系、实体、属性、多片段实体的标注，已经是不错的标注工具了，下面介绍下安装配置过程。

# 1 安装

你可以从brat的官网进行下载：http://brat.nlplab.org/，官网上还有官方的英文[安装介绍](http://brat.nlplab.org/installation.html)可以参考

![image-20210902185623072](%E6%A0%87%E6%B3%A8%E5%B7%A5%E5%85%B7brat%E5%AE%89%E8%A3%85%E5%92%8C%E9%85%8D%E7%BD%AE.assets/image-20210902185623072.png)

下载包

但是我从官网下载链接下载的时候，网络无连接，所以可以从brat的[github仓库](https://github.com/nlplab/brat)下载，两种方法

1. git clone 需要有git环境

   ```shell
   git clone https://github.com/nlplab/brat.git
   ```

2. 下载zip

   ![image-20210902185839531](%E6%A0%87%E6%B3%A8%E5%B7%A5%E5%85%B7brat%E5%AE%89%E8%A3%85%E5%92%8C%E9%85%8D%E7%BD%AE.assets/image-20210902185839531.png)


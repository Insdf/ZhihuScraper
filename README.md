There is an English version of this article: [README_EN](/README_EN.md)
# 目录
[协议](#协议)    

[项目说明](#项目说明)    

[依赖和库](#依赖和库)    

[使用说明](#使用说明)    

[已知问题](#已知问题)    

[写给想零基础自学 Python 爬虫的人](#写给想零基础自学-Python-爬虫的人)    

[知乎上的这篇文章](#知乎上的这篇文章)
# 协议
本项目采用 [GPLv3](/LICENSE) 协议。
# 项目说明
本项目采用 Python 3.10+ 编写，默认运行在 Windows 系统下，使用 Edge 浏览器，使用其他系统和浏览器见后文 [使用说明](#使用说明)。  

本项目爬取知乎公开收藏夹中的内容并保存为 html 文件，包括回答、文章、想法和视频。保存位置默认为 C:\\\_\_assets\_\_\\收藏夹的名字，文件的名字是 作者：标题，想法是以其前 13 个字符为标题。图片和视频是以链接的形式保存，需要联网才能查看，所以保存到本地的内容其实只有文字。  

之所以爬取公开收藏夹是因为私密收藏夹需要登陆知乎后才有权限访问，但我了解到爬取内容过多的话有封号的风险，所以就没有尝试做登陆的功能。另外不登陆爬取知乎内容也有被封 IP 地址的风险，所以我做了一个选择页数的功能，可以输入起始页和终止页来减少每次爬取的数量，比如说一个收藏夹有 20 页，你可以 1\~5，6\~10 这样一次次爬取，中间间隔一段时间，防止被封 IP，注意这里的页数只是我举例用，具体一次爬多少页和多次爬取间隔多少时间不会被封需要你自己尝试。      

开始爬取内容后会有百分比提示，本来想弄一个连续型的，结果弄出来成了离散型的，就是如果有 100 个内容，5 页的话，是 20%, 40%, 60% 这样跳着显示的，不过将就能用吧应该。  

爬虫中有一些预估的时间，不过仅作为参考使用，不一定准确。  

另外有一个想法是用 [you-get](https://github.com/soimort/you-get) 爬取收藏夹图片视频到本地，再用 [html2text](https://github.com/aaronsw/html2text)/[turndown](https://github.com/mixmark-io/turndown)/[sitdown](https://github.com/mdnice/sitdown) 转成 markdown 格式，turndown/sitdown 可能需要在 Python 中调用 Javascript，不过我时间精力有限，有兴趣的话可以自己尝试。  

也尝试过用 concurrent.future 多线程加速，不过效果不太明显，就没有加这个功能。  

本来还想用 pyinstaller 打包一个 exe 文件方便使用，但由于知乎改版频繁，可能发出来没多久就不能用了，所以作罢。  

项目说明就写到这里吧，有什么问题和建议的话请在 Issues 中提。
# 依赖和库
本项目的依赖和库如下，需要下载安装后才能运行本项目中的爬虫：  

[Python 3.10+ (需加入环境变量，建议安装 pip)](https://www.python.org/downloads/)  
[Requests](https://docs.python-requests.org/en/master/user/install/#install)  
[BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/#installing-beautiful-soup)  
[Selenium](https://pypi.org/project/selenium/)  
[Edge浏览器](https://www.microsoft.com/en-us/edge)  
[Edge webdriver (需加入环境变量)](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)  

注意浏览器和 webdriver 的版本匹配。
# 使用说明
首先将项目下载到本地。  

Linux 和 Mac 用户需要将源代码第 22，285 行 (selenium_get_url 函数和 save_html 函数) 中的 folder_path 文件路径改成你想要的路径，注意不要去掉 r' '，只将引号中的路径替换掉就可以了，想的话也可以把第 412，436 行 (主程序) 中 print 提示中有关保存路径的内容改掉，注意用两个斜杠 \\\\ 表示 \\。  

如果你想使用其他浏览器，举个例子，Firefox 浏览器，你需要将第 16，17 行 (即 import 行) 中的 "edge" 改为 "firefox"，将第 72 行 (selenium_get_url函数) 中的 "Edge" 改为 "Firefox"，注意首字母大写。Chrome 和 Safari 同理。对应的 webdriver 下载链接在 [Drivers](https://www.selenium.dev/selenium/docs/api/py/index.html#drivers)  

修改完后，右键 ZhihuCollection.py——打开方式——Python，之后按照程序中的指示就可以了。首先是输入知乎公开收藏夹的地址，注意要求输入的是第一页的网址，且没有 ?page=1 的字样，然后第一次运行要输入浏览器主程序和 webdriver 的路径，注意两个别输反了，然后输入起始页和终止页，等待爬取完成就可以了。  

如果显示的是乱码的话，下载并安装 *VS Code* 并安装 *Python* 和 *Code Runner* 扩展，然后在 *VS Code* 中运行程序 (你可以自己尝试其他编辑器)。对于 *Windows* 用户，打开 Control Panel — Clock and Region — Change data, time or number formats —  Administrative — 将 Language for non-Unicode programs 改为 Chinese simplified — 重启电脑。
# 已知问题
1.知乎改版后就爬取不到内容了。你可以先查看知乎上的值和程序中第 262，276 行 (get_content_detail 函数) 中 class 的值 RichText ztext CopyrightRichText-richText css-14bz7qe 一不一样 (方法在后文)，不一样的话将其改掉，注意改的时候不要去掉引号，只改引号内的内容就可以了。    

更改后的值的话，先随便打开一个收藏夹的网址，选中一个回答的内容
![](https://pic4.zhimg.com/100/v2-cf3f8259f73913da2e17dee3234f5d3b_r.jpeg)  

右键——Inspect (中文名好像叫审查元素吧)
![](https://pic4.zhimg.com/100/v2-54543c0b1a401b829bcc4be4d08eb20f_r.jpeg)  

注意到蓝色的内容
![](https://pic4.zhimg.com/100/v2-f4e631143afa425aaff6e7953e1758cf_r.jpeg)  

点击打开
![](https://pic2.zhimg.com/100/v2-29420fdf4f05509bb8182d38e2d9a551_r.jpeg)
第一个标签中 class 的值就是更改后的值，右键复制就可以了，RichText ztext CopyrightRichText-richText css- 是不变的，就之后的那串字符变了。  

2.多次运行后会莫名其妙地导入 from tkinter.ttk import Progressbar，导致 Selenium 无法正常使用，表现为最大页数爬取出错或无法爬取内容数量，这时在文件开头 import 的地方删除掉就好了。
# 写给想零基础自学 Python 爬虫的人
有很多个理由我推荐你自己学着写一个 Python 爬虫，比如说知乎大规模改版，那这个项目应该就用不了了，而那时我估计已经停止维护这个项目了；或者你想爬取知乎上一个用户底下的所有回答，又或者你想要爬取其他网站上的内容......这些可能都需要你自己来写爬虫。  

选择 Python 写爬虫的原因一个是因为它的语法比较简单，一个是因为有许多现成的库，直接拿来调用就可以了。  

从零基础开始学，每天 2\~3 个小时，大概一个半到两个月就能写出 300 行左右的简单小爬虫。(不包括书中的练习）  

这里推荐两本书和其中有关 Python 基础语法、爬虫基本知识的章节，其他章节有需要的话可以自行翻阅。  

这篇文章写于 2022 年 4 月，隔太久时间看到这篇文章的话，书中的内容可能错误较多 (比如在写文章的这个时间第二本书 11 章中提到的 PhantomJS 浏览器已经不再被 Selenium 支持)，那时可以看看这两本书有没有新版，然后要买这两本书的新版或文章中提到的第二版(没有新版的话)或其他书籍就自己决定吧。    

1\. *PYTHON CRASH COURSE, 2ND EDITION, A Hands-On, Project-Based Introduction to Programming*, by Eric Matthes, No Starch Press. 中译版：《Python编程 从入门到实践 第2版》，人民邮电出版社，第 2-10 章，介绍 Python 的基本语法。  

2\. *Web Scraping with Python, SECOND EDITION, Collecting More Data from the Modern Web*, by Ryan Mitchell, O’Reilly Media. 中译版：《Python网络爬虫权威指南 第2版》，人民邮电出版社，第 1, 2, 10, 11 章，有关 BeautifulSoup, Requests, Selenium 的部分。   

有什么问题的话 bing 搜索，有条件的话 google，中文搜不到用英文，应该能解决绝大多数问题。如果搜不到的话可以在 stackoverflow 上试着问一问。  

这里介绍一个功能，用之前提过的例子
![](https://pic2.zhimg.com/100/v2-29420fdf4f05509bb8182d38e2d9a551_r.jpeg)
`<span class="RichText ztext CopyrightRichText-richText css-14bz7qe" options="[object Object]" itemprop="text">…</span>` 

这里的 span 就是 tag (标签)， = 左边的 class 是 attribute (属性)， = 右边是 attribute 的 value (值)，可以用 BeautifulSoup 中的 find 函数来定位到这个标签，格式是：    

`.find('tag', {'attribute':'value'})`  

这个例子的话就是：    

`.find('span', {'class':'RichText ztext CopyrightRichText-richText css-14bz7qe'})`   

定位后可以通过 get_text() 或 get("attribute") 来获取其中的文本或获取某个属性的值，即：    

`.find('span', {'class':'RichText ztext CopyrightRichText-richText css-14bz7qe'}).get_text()`  

`.find('span', {'class':'RichText ztext CopyrightRichText-richText css-14bz7qe'}).get("attribute")`  

如果用 Requests 获取不到的话，可能是定位的元素是 Javascript 或 css，这里需要用 Selenium 获取内容再通过 find 函数定位。  

注意网页中可能有其他标签、属性和值与你想定位的标签相同，这样的话需要通过其他属性来定位。  

另外如果有需要模拟点击的地方，比如知乎收藏夹页面的“阅读全文”， 可以用 Selenium 中的 click() 方法，不过要通过 Selenium 中的 By 方法来定位。  

最后说一下 robots.txt，如果一个网站的网址是 `https://websites.com`，只要在后面加上 /robots.txt 就可以了，即 `https://websites.com/robots.txt`，里面有关于爬取速率的限制，建议遵守这些限制，以免给服务器造成过大负担。
# 知乎上的这篇文章
这篇文章同步到了知乎上：  
[知乎爬虫：爬取知乎公开收藏夹中的文字内容（视频和图片以链接的形式保存）](https://zhuanlan.zhihu.com/p/500488706)

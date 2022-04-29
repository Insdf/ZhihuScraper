# Table of Contents
[License](#License)  

[Explanation of This Project](#Explanation-of-This-Project)  

[Dependencies and Libraries](#Dependencies-and-Libraries)  

[Instructions for Use](#Instructions-for-Use)  

[Known Issues](#Known-Issues)  

[For Those Who Want to Learn Python Crawler by Themselves From Scratch](#For-Those-Who-Want-to-Learn-Python-Crawler-by-Themselves-From-Scratch)  

[This Article on Blogger](#This-Article-on-Blogger)
# License
This project uses the [GPLv3](/LICENSE) license.
# Explanation of This Project
This project is written in Python 3.10+, runs on *Windows* by default, and uses the *Edge* browser. For other systems and browsers, see [Instructions for Use](#Instructions-for-Use).  

This project crawls the content in Zhihu's public collection folder and saves it as an html file, including answers, articles, pins, and videos. The save location defaults to C:\\\_\_assets\_\_\\the name of the collection folder, the name of the file is Author: Title and for the pin it uses its first 13 characters as the title. Pictures and videos are saved in the form of links and need to be connected to the Internet to view, so the content saved locally is actually only text.

The reason for crawling public collecion folder is that private collecion folder need to be logged in to Zhihu before they can be accessed, but I learn about that crawling too much content has the risk of the account being banned, so I did not try to write a log in feature. In addition, if you don’t log in to crawl Zhihu content, there is also the risk of your IP address being blocked, so I made a feature to select the number of pages. You can input the start page and end page to reduce the amount of crawling each time. For example, a collecion folder has 20 pages, you can crawl 1\~5, 6\~10, etc, with a period of time in between, to prevent IP from being blocked. Note that the number of pages here is just for my example, how many pages to crawl at one time and how mucn time to suspend between multi crawling won't be blocked requires you to try it yourself.

After starting to crawl the content, there will be a percentage prompt. I originally wanted to make a continuous type, but it turned out to be a discrete type, that is, if there are 100 content and 5 pages, it shows 20%, 40%, 60%, etc, but it should work.

There are some estimated time in the crawler, but they are only reference points and may not be accurate.

I had an idea to use [*you-get*](https://github.com/soimort/you-get) to crawl the pictures and videos of the collecion folder to the local, and then use [*html2text*](https://github.com/aaronsw/html2text)/[*turndown*](https://github.com/mixmark-io/turndown)/[*sitdown*](https://github.com/mdnice/sitdown) to convert the html to markdown format, *turndown/sitdown* may need to call *Javascript* in *Python*, but I have limited time and energy, if you are interested, you can try it yourself.

I have also tried to use *concurrent.future* multi-thread acceleration, but the effect is not obvious, so this feature is not added.

Originally, I wanted to use *pyinstaller* to package an *exe* file for easy use, but due to frequent revisions of Zhihu, it may not work soon after it was released, so I gave it up.

The explanation of this project is done. If you have any questions and suggestions, please mention them in Issues.
# Dependencies and Libraries
The dependencies and libraries of this project are as follows, and you should download and install them before run the scraper in this project:

[Python 3.10+ (need to add to path, and it is recommended to install pip)](https://www.python.org/downloads/)  
[Requests](https://docs.python-requests.org/en/master/user/install/#install)  
[BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/#installing-beautiful-soup)  
[Selenium](https://pypi.org/project/selenium/)  
[Edge browser](https://www.microsoft.com/en-us/edge)  
[Edge webdriver (need to add to path)](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

Note that the browser and webdriver versions match.
# Instructions for Use
First download the project locally.

Linux and Mac users need to modify the *folder_path* in line 22, 285 of the source code (*selenium_get_url* function and *save_html* function) to the path you want, be careful not to remove r' ', just replace the path in quotation marks. If you want, you can also modify the content about the save path in the *print* prompt in line 412 and 436 (main program), pay attention to use two backslashes \\\\ to represent \\.

If you want to use other browsers, for example, *Firefox* browser, you need to modify "edge" in lines 16, 17 (ie import lines) to "firefox", and in line 72 (*selenium_get_url* function), modify "Edge" to "Firefox", note the capitalization. The same goes for *Chrome* and *Safari*. The corresponding webdriver download link is at [Drivers](https://www.selenium.dev/selenium/docs/api/py/index.html#drivers)

After modification, Right-click ZhihuCollection_EN.py — Open with — Python, and then follow the instructions in the program. The first is to input the address of Zhihu's public collection folder. Note that the URL of the first page is required to be inputted, and there is no word *?page=1*. Then, for the first run, you need to input the path of the browser main program and webdriver. Don't type them in reverse. Then input the start page and end page, and wait for the crawling to complete.

If it shows garbage characters in the name of the collection folder, download and install *VS Code* and install *Python* and *Code Runner* extensions, then run the program in *VS Code* (You can try other editors by yourself). For *Windows* users, Open Control Panel — Clock and Region — Change data, time or number formats —  Administrative — Change Language for non-Unicode programs to Chinese simplified — Restart.
# Known Issues
1\. After the revision of Zhihu, the content cannot be crawled. You can first check that if the value on Zhihu is different from the value "RichText ztext CopyrightRichText-richText css-14bz7qe" of *class* in line 262 and 276 (*get_content_detail* function) in the program (the instruction is in later section), if it is different, modify it. Be careful not to remove the quotation marks when modifying, just modify the content within the quotation marks.

For the new value, first open a URL of a collection folder, and select the content of an answer.
![](https://pic4.zhimg.com/100/v2-cf3f8259f73913da2e17dee3234f5d3b_r.jpeg)

Right-click — Inspect
![](https://pic4.zhimg.com/100/v2-54543c0b1a401b829bcc4be4d08eb20f_r.jpeg)

Notice the blue content
![](https://pic4.zhimg.com/100/v2-f4e631143afa425aaff6e7953e1758cf_r.jpeg)

Click to open
![](https://pic2.zhimg.com/100/v2-29420fdf4f05509bb8182d38e2d9a551_r.jpeg)
The value of *class* in the first tag is the new value. Right-click to copy it. "RichText ztext CopyrightRichText-richText css-" is unchanged, and the string of characters after that has changed.

2\. After multiple runs, *from tkinter.ttk import Progressbar* will be imported inexplicably, which will cause *Selenium* to fail to work properly. And the maximum number of pages crawled is wrong, or it can't get the amount of contents. At this time, just delete it at the *import* lines at the beginning of the file.
# For Those Who Want to Learn Python Crawler by Themselves From Scratch
There are many reasons why I recommend that you learn to write a Python crawler yourself. For example, if Zhihu makes a large-scale revision, then this project should be useless, and I guess I have stopped maintaining this project at that time; or you want to crawl all the answers under an user in Zhihu, or you want to crawl content from other websites... These may require you to write a crawler yourself.

One of the reasons for choosing *Python* to write a crawler is because its syntax is relatively simple, and the other is because there are many ready-made libraries, which can be called directly.

Start learning from scratch, 2\~3 hours a day, about one and a half to two months, you can write a simple crawler with about 300 lines.(does not include exercises in the book)  

I recommend two books and their chapters on basic *Python* syntax and crawler knowledge here. You can read other chapters if you need them.

This article was written in April 2022. If you read this article after a long time, there may be many mistakes in the books (for example, the *PhantomJS* browser mentioned in Chapter 11 in the second book is no longer supported by *Selenium* at the time of writing this article), then you can see if there are new editions of these two books, and then decide whether to buy the new editions of these two books or the second edition mentioned in the article (if there is no new edition) or the other books. .

1\. *PYTHON CRASH COURSE, 2ND EDITION, A Hands-On, Project-Based Introduction to Programming*, by Eric Matthes, No Starch Press. Chapters 2-10, introduces the basic syntax of Python.

2\. *Web Scraping with Python, SECOND EDITION, Collecting More Data from the Modern Web*, by Ryan Mitchell, O'Reilly Media. Chapters 1, 2, 10, 11, sections on *BeautifulSoup*, *Requests* and *Selenium*.

If there is any problem, *bing* or *google* it, it should be able to solve most of the problems. If you can't find any answer, try to ask your question on *stackoverflow*.  

Introduce a function here, using the example mentioned earlier
![](https://pic2.zhimg.com/100/v2-29420fdf4f05509bb8182d38e2d9a551_r.jpeg)
`<span class="RichText ztext CopyrightRichText-richText css-14bz7qe" options="[object Object]" itemprop="text">…</span>`

The *span* here is the *tag*, the *class* on the left of the = is the *attribute*, and the right side of the = is the *value* of the *attribute*. You can use the *find* function in *BeautifulSoup* to locate this tag. The format is:

`.find('tag', {'attribute':'value'})`

This example is:

`.find('span', {'class':'RichText ztext CopyrightRichText-richText css-14bz7qe'})`  

Note that before locating, use view source to view the page source code or print out the page source code, and make sure that there is the tag you want to locate, otherwise it will show that the element cannot be found.

After locating, you can use *get_text()* or *get("attribute")* to get the text in it or get the value of an attribute, that is:

`.find('span', {'class':'RichText ztext CopyrightRichText-richText css-14bz7qe'}).get_text()`

`.find('span', {'class':'RichText ztext CopyrightRichText-richText css-14bz7qe'}).get("attribute")`

If you can't get it with *Requests*, it may be that the element to be located is *Javascript* or *CSS*. Here, you need to use *Selenium* to get the content and then locate it through the *find* function.

Note that there may be other tags that have the same *tag*, *attribute* and *value* as the tag you want to locate, so you need to locate them through other attributes.

In addition, if there is a place where you need to simulate a click, such as "reading the full text" on the Zhihu collection folder page, you can use the *click()* method in *Selenium*, but you need to locate it through the *By* method in *Selenium*.

Finally, let’s talk about robots.txt. If the URL of a website is `https://websites.com`, just add `/robots.txt` after it, that is, `https://websites.com/robots.txt` , which has a limit on the crawling rate. It is advisable to obey these limits to not overburden the server.
# This Article on Blogger
This article is posted on Blogger as well:  
[Zhihu Scraper: Scraping the text content in Zhihu's public collection folder (Videos and pictures are saved in the form of links)](https://rei159.blogspot.com/2022/04/zhihu-scraper-scraping-text-content-in.html)

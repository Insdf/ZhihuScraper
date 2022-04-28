"""
该程序 ZhihuCollection 的原作者是 Insdf。
该程序是在 General Public License version 3 下发布的。
您应该已经收到了一份通用公共许可证文本的副本以及该程序。 如果没有，您可以从 https://www.gnu.org/licenses/gpl-3.0.html 获取。
本程序不提供任何担保，作者对本程序造成的任何损坏或问题概不负责。
"""

import re
import os
import math
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# 使用 selenium 获取 html 内容。（非页面源代码）
def selenium_get_url(url):
    
    folder_path = r"C:\__assets__"
    if os.path.exists(folder_path):
        pass
    else:
        os.makedirs(folder_path)

    browser_path_txt = rf"{folder_path}\browser_path.txt"
    webdriver_path_txt = rf"{folder_path}\webdriver_path.txt"
    
    if os.path.exists(browser_path_txt):
        with open(browser_path_txt, 'r', encoding='utf-8') as file:
            browser_path = file.read()
            browser_path = repr(browser_path)
            browser_path = re.sub('\'', '', browser_path)
    else:
        print("\n第一次运行需要输入浏览器主程序和webdriver主程序路径，之后两个路径保存在 C:\\__assets__ 中，无需再输入，不要删除或移动它们。")
        browser_path = input("\n请输入浏览器主程序所在路径，输入后按回车: ")
        with open(browser_path_txt, 'a', encoding='utf-8') as file:
            file.write(browser_path)
        browser_path = repr(browser_path)
        browser_path = re.sub('\'', '', browser_path)

    if os.path.exists(webdriver_path_txt):
        with open(webdriver_path_txt, 'r', encoding='utf-8') as file:
            webdriver_path = file.read()
            webdriver_path = repr(webdriver_path)
            webdriver_path = re.sub('\'', '', webdriver_path)
    else:
        webdriver_path = input("请输入webdriver主程序所在路径，输入后按回车，并等待大约30秒: ")
        with open(webdriver_path_txt, 'a', encoding='utf-8') as file:
            file.write(webdriver_path)
        webdriver_path = repr(webdriver_path)
        webdriver_path = re.sub('\'', '', webdriver_path)

    # 参数 executable_path 被添加到 Service 函数中，所以这里使用 Service。
    service = Service(executable_path=webdriver_path)

    # 使用 Options 函数使程序正常运行。请注意，路径中应该有两个“\”。
    options = Options()
    options.binary_location = browser_path

    # 去掉 Devtool listening.
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # 阻止浏览器弹出。
    options.add_argument("--headless")

    # 伪装成浏览器。
    options.add_argument('user-agent="Mozilla/5.0"')

    driver = webdriver.Edge(service=service, options=options)
    driver.get(url)
    time.sleep(2)

    # 获取到 url 后数据存储在 driver 中，所以在此处返回driver。
    return driver

# 使用 requests 获取 html 内容。
def get_html(url):

    headers = {
        'Referer': url,
        'User-Agent': 'Mozilla/5.0'
    } 
    html = requests.get(url, headers=headers)
    bs = BeautifulSoup(html.content, 'html.parser')
    return bs

# 获取 url 的 javascript、css 或 html 内容。页码是用 JavaScript 编写的，你应该使用 selenium 来提取它们。
def get_js_css_in_html(url):

    driver = selenium_get_url(url)
    pageSource = driver.page_source
    driver.quit()
    bs = BeautifulSoup(pageSource, 'html.parser')
    return bs

# 获取收藏的最大页码。
def get_collection_max_page(url):

    page_list_numbers = []
    page_lists = []  
    page_caches = get_js_css_in_html(url).find_all('button', {'class':'Button PaginationButton Button--plain'})

    # 如果收藏夹中只有 1 页。 
    if page_caches == []:
        print("\n最大页数: 1")
        return 1

    else:
        for page_cache in page_caches:
            page_lists.append(page_cache.get_text())
        for page_list in page_lists:
            page_list_numbers.append(int(page_list))

    max_page = max(page_list_numbers)
    print(f"最大页数: {max_page}")
    return max_page

# 得到收藏夹的标题。
def get_collection_title(url):

    title = get_html(url).find('div', {'class':'CollectionDetailPageHeader-title'}).get_text() 
    print(f"\n收藏夹名字: {title}")
    return title

# 得到收藏夹中的内容数量。
def get_collection_quantity(url):

    quantity_cache = get_js_css_in_html(url).find('div', {'class':'Card-headerText'}).get_text()
    pattern = re.compile("[^0-9]*")
    quantity_cache = re.sub(pattern, '', quantity_cache) 
    quantity = int(quantity_cache)
    print(f"内容数量: {quantity}")
    return quantity

# 根据起始页和结束页获取内容的数量。
def get_real_content_quantity(start_page, end_page, max_page, collection_quantity):

    if start_page == 1 and end_page < max_page:
        quantity = end_page * 20
    elif start_page != 1 and end_page < max_page:
        quantity = (end_page - start_page + 1) * 20
    elif end_page == max_page:
        quantity = collection_quantity - (start_page - 1) * 20
    return quantity

# 获取得到内容的时间成本。
def get_content_cost_time(start_page, end_page, max_page, collection_quantity):

    if start_page == 1 and end_page < max_page:
        quantity = end_page * 20
    elif start_page != 1 and end_page < max_page:
        quantity = (end_page - start_page + 1) * 20
    elif end_page == max_page:
        quantity = collection_quantity - (start_page - 1) * 20
    content_seconds = quantity * 10
    return content_seconds

# Windows 操作系统中不能使用非法字符作为文件名，所以使用正则表达式替换为全角字符。
def replace_illegal_char(title):

    title = re.sub("\\\\", "＼", title)
    title = re.sub("/", "／", title)
    title = re.sub(":", "：", title)
    title = re.sub("\?", "？", title)
    title = re.sub("\*", "＊", title)
    title = re.sub("\"", "＂", title)
    title = re.sub("<", "＜", title)
    title = re.sub(">", "＞", title)
    title = re.sub("\|", "｜", title)
    return title

# 得到一部分页面源代码中的内容细节的标题。
def get_content_detail_title(bs_list, content=None, video=False):
    
    # 如果是一个想法。
    if content != None:
        pattern = re.compile("<.*?>")
        content_txt = re.sub(pattern, "", f"{content}")

        # 使用前 13 个字符作为标题。
        title = content_txt[0:13]

        title = replace_illegal_char(title)
        return title

    # 如果不是一个视频。
    elif video == False:

        title = bs_list.find('a', {'data-za-detail-view-element_name': "Title"}).get_text()
        title = replace_illegal_char(title)
        return title

    # 如果是一个视频。
    elif video == True:

        title = bs_list.find('a', {'rel': "noopener noreferrer"}).get_text()
        title = replace_illegal_char(title)
        return title

# 得到一部分页面源代码中的回答者。
def get_answerer(bs_list):

    answerer = bs_list.find('img', {'class': "Avatar AuthorInfo-avatar"}).get('alt')
    return answerer

# 替换视频来让它显示。
def replace_video(content):

    flag = re.search("""<div><div class="RichText-video".*?class="VideoCard-mask"></div></div></div></div>""", f"{content}")
    pattern = re.compile("""<div><div class="RichText-video".*?class="VideoCard-mask"></div></div></div></div>""")

    while flag != None:
        video_id = re.search("\"video_id\":\".*?\"", f"{content}").group(0)
        id = re.search("\d.*\d", video_id).group(0)
        src = f"https://video.zhihu.com/video/{id}"
        src = f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><a href=\"{src}\">{src}</a></body></html>"""

        # 注意添加 count=1，这意味着只需替换第一个匹配项。
        content = re.sub(pattern, src, f"{content}", count=1)

        flag = re.search("""<div><div class="RichText-video".*?class="VideoCard-mask"></div></div></div></div>""", f"{content}")
    return content

# 替换链接来让它显示。
def replace_link(content):

    flag1 = re.search("""data-za-detail-view-id="172" href=.*? target="_blank">""", f"{content}")
    flag2 = re.search("""data-text="(?!true)(?!.*?data-tooltip).*?href=.*?target="_blank">""", f"{content}")

    pattern1 = re.compile("""data-za-detail-view-id="172" href=.*? target="_blank">""")
    pattern2 = re.compile("""data-text="(?!true)(?!.*?data-tooltip).*?href=.*?target="_blank">""")

    while flag1 != None or flag2 != None:
        if re.search("data-za-detail-view-id=\"172\" href=\".*?\"", f"{content}") != None:
            text = re.search("data-za-detail-view-id=\"172\" href=\".*?\"", f"{content}").group(0)
            href = re.search("https://.*[0-9a-zA-Z]|http://.*[0-9a-zA-Z]", text).group(0)
            href = f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><a href=\"{href}\">{href}</a></body></html>"""
            content = re.sub(pattern1, href, f"{content}", count=1)
    
        if re.search("""data-text="(?!true)(?!.*?data-tooltip).*?href=.*?target="_blank">""", f"{content}") != None:

            # 注意添加 text.group(0) 来获取 search 的文本。
            text = re.search("""data-text="(?!true)(?!.*?data-tooltip).*?href=.*?target="_blank">""", f"{content}").group(0)
            href = re.search("https://.*?\"|http://.*?\"", text).group(0)
            href = re.search("https://.*[0-9a-zA-Z]|http://.*[0-9a-zA-Z]", href).group(0)
            href = f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><a href=\"{href}\">{href}</a></body></html>"""
            content = re.sub(pattern2, href, f"{content}", count=1)

        flag1 = re.search("""data-za-detail-view-id="172" href=.*? target="_blank">""", f"{content}")
        flag2 = re.search("""data-text="(?!true)(?!.*?data-tooltip).*?href=.*?target="_blank">""", f"{content}")
    return content

# 得到一部分页面源代码中的内容。
def get_content_detail(bs_list, video=False):
   
    # 如果不是一个视频。
    if video == False:

        content = bs_list.find('span', {'class': "RichText ztext CopyrightRichText-richText css-14bz7qe"})
        flag = re.search("""<div><div class="RichText-video".*?class="VideoCard-mask"></div></div></div></div>""", f"{content}")
        if flag != None:
            content = replace_video(content)
        flag1 = re.search("""data-za-detail-view-id="172" href=.*? target="_blank">""", f"{content}")
        flag2 = re.search("""data-text="(?!true)(?!.*?data-tooltip).*?href=.*?target="_blank">""", f"{content}")
        if flag1 != None or flag2 != None:
            content = replace_link(content)
        return content

    # 如果是一个视频。
    elif video == True:

        content_link = bs_list.find('a', {'rel': "noopener noreferrer"}).get('href')    
        content_word = bs_list.find('span', {'class': "RichText ztext CopyrightRichText-richText css-14bz7qe"})
        content1 = f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><a href=\"{content_link}\">{content_link}</a></body></html>"""
        content2 = f"\n{content_word}"
        content = content1 + content2
        return content

# 保存内容为 html.
def save_html(collection_title, answerer, content, title):
 
    folder_path = rf'C:\__assets__\{collection_title}'

    # 检查文件夹是否存在。
    if os.path.exists(folder_path):
        pass
    # 文件夹不存在。
    else:
        os.makedirs(folder_path)

    file_path = f'{folder_path}/{answerer}：{title}.html'

    # 检查文件是否存在。
    if os.path.exists(file_path):
        pass

    # 文件不存在。
    else:

        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"{content}")

# 获取 url 的详细内容。   
def get_contents(url, collection_title, real_content_quantity):

    driver = selenium_get_url(url)
    try:
        button = driver.find_element(By.CSS_SELECTOR, '.ContentItem-more')
        while button != None:
            button.click()
            button = driver.find_element(By.CSS_SELECTOR, '.ContentItem-more') 
    except:
        pass  

    pageSource = driver.page_source
    bs = BeautifulSoup(pageSource, 'html.parser')
    driver.quit() 

    global process_indicator

    # 查找 url 中的所有内容。
    bs_lists = bs.find_all('div', {'class':"CollectionDetailPageItem-innerContainer"})

    for bs_list in bs_lists:
        
        # 如果是一个想法。
        if bs_list.find('div', {'class':'ContentItem PinItem'}) != None:

            answerer = get_answerer(bs_list) 
            content = get_content_detail(bs_list)
            title = get_content_detail_title(bs_list, content)
            save_html(collection_title, answerer, content, title)
            process_indicator += 1
            process = process_indicator / real_content_quantity * 100
            print("\r已完成 %.2f%%" %process, end='')
        
        # 如果是一个文章。
        elif bs_list.find('div', {'class':'ContentItem ArticleItem'}) != None:

            title = get_content_detail_title(bs_list)
            answerer = get_answerer(bs_list)   
            content = get_content_detail(bs_list)
            save_html(collection_title, answerer, content, title)
            process_indicator += 1
            process = process_indicator / real_content_quantity * 100
            print("\r已完成 %.2f%%" %process, end='')

        # 如果是一个视频。请注意，视频中标题和内容的位置与其他项不同。  
        elif bs_list.find('div', {'class':'ContentItem ZVideoItem'}) != None:
            title = get_content_detail_title(bs_list, video=True)
            answerer = get_answerer(bs_list)   
            content = get_content_detail(bs_list, video=True)
            save_html(collection_title, answerer, content, title)
            process_indicator += 1
            process = process_indicator / real_content_quantity * 100
            print("\r已完成 %.2f%%" %process, end='')

        # 如果是一个回答。
        elif bs_list.find('div', {'class':'ContentItem AnswerItem'}) != None:   
            
            title = get_content_detail_title(bs_list)
            answerer = get_answerer(bs_list)   
            content = get_content_detail(bs_list)
            save_html(collection_title, answerer, content, title)  
            process_indicator += 1
            process = process_indicator / real_content_quantity * 100
            print("\r已完成 %.2f%%" %process, end='')

# 如果这个文件作为主程序运行（不是由其他文件导入的），下面的代码将被执行。
if __name__ == "__main__":
    
    url_original = input("请输入知乎公开收藏夹的地址，输入后按回车: ")
    print("\n在已保存浏览器及webdriver路径的情况下(第二次及之后运行)请等待大约30秒...")
    get_js_css_in_html(url_original)
    print("\n先爬取收藏夹的最大页数和内容数量，距开始爬取内容预计还有 1 分钟，请耐心等待，之后有需要输入的操作...")
    
    start_time = time.time()
    max_page = get_collection_max_page(url_original)
    collection_quantity = get_collection_quantity(url_original)
    
    end_time = time.time()
    cost_time = end_time - start_time
    minute = math.floor(cost_time / 60)
    second = cost_time % 60
    print(f"\n爬取收藏夹最大页数和内容数量用时: {minute}分钟, {second}秒钟。")

    # 防止你在没有输入的情况下按回车。
    flag = True
    while flag:
        start_page = input(f"\n请输入起始页(范围：1~{max_page})，输入后按回车: ")
        if start_page != '':
            flag = False
    flag = True
    while flag:
        end_page = input(f"请输入终止页(范围：{start_page}~{max_page})，输入后按回车: ")
        if end_page != '':
            flag = False        

    # 从输入中获得的 start_page 和 end_page 是字符串，因此请将它们转换为整数。
    start_page = int(start_page)
    end_page = int(end_page)

    content_seconds = get_content_cost_time(start_page, end_page, max_page, collection_quantity)
    page_seconds = (end_page - start_page) * 10
    total_seconds = content_seconds + page_seconds
    minute = math.floor(total_seconds / 60)
    second = total_seconds % 60

    print(f"\n开始爬取内容，预计需要花费 {minute}分钟{second}秒钟，现在你可以做一些其他的事情，不要关闭界面，你可以在本界面中查看百分比进度，也可以在 C:\\__assets__ 中查看已爬取的内容，爬取完成后会有\"爬取完成。\"的字样提示...")  

    start_time = time.time()
    collection_title = get_collection_title(url_original)

    global process_indicator
    process_indicator = 0

    real_content_quantity = get_real_content_quantity(start_page, end_page, max_page, collection_quantity)
    print(f"\n实际爬取数量: {real_content_quantity}\n")

    process = process_indicator / real_content_quantity * 100
    print("\r已完成 %.2f%%" %process, end='')
    
    for i in range(start_page, end_page+1):
        url = f"{url_original}?page={str(i)}"
        get_contents(url, collection_title, real_content_quantity)
        time.sleep(10)

    print("\n\n爬取完成。")
    end_time = time.time()
    cost_time = end_time - start_time
    minute = math.floor(cost_time / 60)
    second = cost_time % 60
    print(f"爬取内容用时: {minute}分钟, {second}秒钟，现在你可以关闭界面，并在  C:\\__assets__\\{collection_title} 中查看已爬取的内容。")
    input()

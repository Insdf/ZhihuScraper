"""
The original author of this program, ZhihuScraper, is Insdf.
This program is released under General Public License version 3.
You should have received a copy of General Public License text alongside with this program. If not, you can obtain it at https://www.gnu.org/licenses/gpl-3.0.html.
This program comes with no warranty, the author will not be resopnsible for any damage or problems caused by this program.
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

# Use selenium to get html content. (not the page source)
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
        print("\nFor the first run, you need to input the paths of the browser main program and the webdriver, then the two paths are saved in C:\\__assets__ and you need not to input again. Do not delete or move them.")
        browser_path = input("\nPlease input the path where the browser main program is located, and press Enter after inputting: ")
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
        webdriver_path = input("Please input the path where the webdriver main program is located, press Enter after inputting, and wait for about 30 seconds: ")
        with open(webdriver_path_txt, 'a', encoding='utf-8') as file:
            file.write(webdriver_path)
        webdriver_path = repr(webdriver_path)
        webdriver_path = re.sub('\'', '', webdriver_path)

    # The parameter executable_path is added to Serivice function, so use Service here.
    service = Service(executable_path=webdriver_path)

    # Use Options function to run the program normally. Note that there should be two '\' in the path.
    options = Options()
    options.binary_location = browser_path

    # To remove Devtool listening.
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # To prevent the browser to pop up.
    options.add_argument("--headless")

    # Disguise to be a browser.
    options.add_argument('user-agent="Mozilla/5.0"')

    driver = webdriver.Edge(service=service, options=options)
    driver.get(url)
    time.sleep(2)

    # The data is stored in driver after getting url, so return driver here.
    return driver

# Get html contents using requests.
def get_html(url):

    headers = {
        'Referer': url,
        'User-Agent': 'Mozilla/5.0'
    } 
    html = requests.get(url, headers=headers)
    bs = BeautifulSoup(html.content, 'html.parser')
    return bs

# To get the javascript, css or html contents of the url. The page numbers are written in JavaScript, and you should use selenium to extract them.
def get_js_css_in_html(url):

    driver = selenium_get_url(url)
    pageSource = driver.page_source
    driver.quit()
    bs = BeautifulSoup(pageSource, 'html.parser')
    return bs

# Get the max page number of the collection.
def get_collection_max_page(url):

    page_list_numbers = []
    page_lists = []  
    page_caches = get_js_css_in_html(url).find_all('button', {'class':'Button PaginationButton Button--plain'})

    # If there is only one page in the collection folder. 
    if page_caches == []:
        print("\nMaximum number of pages: 1")
        return 1

    else:
        for page_cache in page_caches:
            page_lists.append(page_cache.get_text())
        for page_list in page_lists:
            page_list_numbers.append(int(page_list))

    max_page = max(page_list_numbers)
    print(f"\nMaximum number of pages: {max_page}")
    return max_page

# Get the title of the collection folder.
def get_collection_title(url):

    title = get_html(url).find('div', {'class':'CollectionDetailPageHeader-title'}).get_text() 
    print(f"\nThe name of the collection folder: {title}")
    return title

# Get the quantity of cotent in the collection folder.
def get_collection_quantity(url):

    quantity_cache = get_js_css_in_html(url).find('div', {'class':'Card-headerText'}).get_text()
    pattern = re.compile("[^0-9]*")
    quantity_cache = re.sub(pattern, '', quantity_cache) 
    quantity = int(quantity_cache)
    print(f"Amount of content: {quantity}")
    return quantity

# Get the quantity of the contents according to the start page and end page.
def get_real_content_quantity(start_page, end_page, max_page, collection_quantity):

    if start_page == 1 and end_page < max_page:
        quantity = end_page * 20
    elif start_page != 1 and end_page < max_page:
        quantity = (end_page - start_page + 1) * 20
    elif end_page == max_page:
        quantity = collection_quantity - (start_page - 1) * 20
    return quantity

# Get the cost of time of getting contents.
def get_content_cost_time(start_page, end_page, max_page, collection_quantity):

    if start_page == 1 and end_page < max_page:
        quantity = end_page * 20
    elif start_page != 1 and end_page < max_page:
        quantity = (end_page - start_page + 1) * 20
    elif end_page == max_page:
        quantity = collection_quantity - (start_page - 1) * 20
    content_seconds = quantity * 10
    return content_seconds

# Illegal characters can't be used as file name in windows os, so use regular expression to replace them with full-width characters.
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

# Get the content detail title of a part of page source.
def get_content_detail_title(bs_list, content=None, video=False):
    
    # If it is a pin.
    if content != None:
        pattern = re.compile("<.*?>")
        content_txt = re.sub(pattern, "", f"{content}")

        # Use the first 13 characters as the title.
        title = content_txt[0:13]

        title = replace_illegal_char(title)
        return title

    # If it is not a video.
    elif video == False:

        title = bs_list.find('a', {'data-za-detail-view-element_name': "Title"}).get_text()
        title = replace_illegal_char(title)
        return title

    # If it is a video.
    elif video == True:

        title = bs_list.find('a', {'rel': "noopener noreferrer"}).get_text()
        title = replace_illegal_char(title)
        return title

# Get the answerer of a part of page source.
def get_answerer(bs_list):

    answerer = bs_list.find('img', {'class': "Avatar AuthorInfo-avatar"}).get('alt')
    return answerer

# Replace the video to let it show.
def replace_video(content):

    flag = re.search("""<div><div class="RichText-video".*?class="VideoCard-mask"></div></div></div></div>""", f"{content}")
    pattern = re.compile("""<div><div class="RichText-video".*?class="VideoCard-mask"></div></div></div></div>""")

    while flag != None:
        video_id = re.search("\"video_id\":\".*?\"", f"{content}").group(0)
        id = re.search("\d.*\d", video_id).group(0)
        src = f"https://video.zhihu.com/video/{id}"
        src = f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><a href=\"{src}\">{src}</a></body></html>"""

        # Note to add count=1, which means just replace the first match.
        content = re.sub(pattern, src, f"{content}", count=1)

        flag = re.search("""<div><div class="RichText-video".*?class="VideoCard-mask"></div></div></div></div>""", f"{content}")
    return content

# Replace the link to let it show.
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

            # Note to add text.group(0) to get the text of search.
            text = re.search("""data-text="(?!true)(?!.*?data-tooltip).*?href=.*?target="_blank">""", f"{content}").group(0)
            href = re.search("https://.*?\"|http://.*?\"", text).group(0)
            href = re.search("https://.*[0-9a-zA-Z]|http://.*[0-9a-zA-Z]", href).group(0)
            href = f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><a href=\"{href}\">{href}</a></body></html>"""
            content = re.sub(pattern2, href, f"{content}", count=1)

        flag1 = re.search("""data-za-detail-view-id="172" href=.*? target="_blank">""", f"{content}")
        flag2 = re.search("""data-text="(?!true)(?!.*?data-tooltip).*?href=.*?target="_blank">""", f"{content}")
    return content

# Get the content of a part of page source.
def get_content_detail(bs_list, video=False):
   
    # If it is not a video.
    if video == False:

        content = bs_list.find('span', {'class': "RichText ztext CopyrightRichText-richText css-9scqi7"})

        # Resize the image.
        pattern = re.compile(" width=\"[0-9]*?\"")
        content = re.sub(pattern, ' width=\"600\"', f"{content}")

        flag = re.search("""<div><div class="RichText-video".*?class="VideoCard-mask"></div></div></div></div>""", f"{content}")
        if flag != None:
            content = replace_video(content)
        flag1 = re.search("""data-za-detail-view-id="172" href=.*? target="_blank">""", f"{content}")
        flag2 = re.search("""data-text="(?!true)(?!.*?data-tooltip).*?href=.*?target="_blank">""", f"{content}")
        if flag1 != None or flag2 != None:
            content = replace_link(content)
        return content

    # If it is a video.
    elif video == True:

        content_link = bs_list.find('a', {'rel': "noopener noreferrer"}).get('href')    
        content_word = bs_list.find('span', {'class': "RichText ztext CopyrightRichText-richText css-9scqi7"})
        content1 = f"""<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><a href=\"{content_link}\">{content_link}</a></body></html>"""
        content2 = f"\n{content_word}"
        content = content1 + content2
        return content

# Save contents to html.
def save_html(collection_title, answerer, content, title):
 
    folder_path = rf'C:\__assets__\{collection_title}'

    # To check if the folder is existed.
    if os.path.exists(folder_path):
        pass
    # The folder is not existed.
    else:
        os.makedirs(folder_path)

    file_path = f'{folder_path}/{answerer}：{title}.html'

    # To check if the file is existed.
    if os.path.exists(file_path):
        pass

    # File is not existed.
    else:

        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"{content}")

# Get the detail contents of the url.    
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

    # Find all contents in a url.
    bs_lists = bs.find_all('div', {'class':"CollectionDetailPageItem-innerContainer"})

    for bs_list in bs_lists:
        
        # If it is a pin.
        if bs_list.find('div', {'class':'ContentItem PinItem'}) != None:

            answerer = get_answerer(bs_list) 
            content = get_content_detail(bs_list)
            title = get_content_detail_title(bs_list, content)
            save_html(collection_title, answerer, content, title)
            process_indicator += 1
            process = process_indicator / real_content_quantity * 100
            print("\r%.2f%% completed" %process, end='')
        
        # If it is an article.
        elif bs_list.find('div', {'class':'ContentItem ArticleItem'}) != None:

            title = get_content_detail_title(bs_list)
            answerer = get_answerer(bs_list)   
            content = get_content_detail(bs_list)
            save_html(collection_title, answerer, content, title)
            process_indicator += 1
            process = process_indicator / real_content_quantity * 100
            print("\r%.2f%% completed" %process, end='')

        # If it is a video. Note that the location of the title and the content in a video is different from other items.   
        elif bs_list.find('div', {'class':'ContentItem ZVideoItem'}) != None:
            title = get_content_detail_title(bs_list, video=True)
            answerer = get_answerer(bs_list)   
            content = get_content_detail(bs_list, video=True)
            save_html(collection_title, answerer, content, title)
            process_indicator += 1
            process = process_indicator / real_content_quantity * 100
            print("\r%.2f%% completed" %process, end='')

        # If it is an answer.
        elif bs_list.find('div', {'class':'ContentItem AnswerItem'}) != None:   
            
            title = get_content_detail_title(bs_list)
            answerer = get_answerer(bs_list)   
            content = get_content_detail(bs_list)
            save_html(collection_title, answerer, content, title)  
            process_indicator += 1
            process = process_indicator / real_content_quantity * 100
            print("\r%.2f%% completed" %process, end='')

# If this file runs as the main program (not imported by other file), the codes below will be executed.
if __name__ == "__main__":
    
    url_original = input("Please input the address of Zhihu's public collection folder, and press Enter after inputting: ")
    print("\nPlease wait about 30 seconds with the browser and webdriver paths saved (for the second and subsequent runs)...")
    get_js_css_in_html(url_original)
    print("\nCrawling the maximum number of pages and the amount of content of the collection folder first, it is estimated that there will be 1 minute before starting to crawl the content, please wait patiently, and then there are inputting operations later...")
    
    start_time = time.time()
    max_page = get_collection_max_page(url_original)
    collection_quantity = get_collection_quantity(url_original)
    
    end_time = time.time()
    cost_time = end_time - start_time
    minute = math.floor(cost_time / 60)
    second = cost_time % 60
    print(f"\nTime cost of crawling the maximum number of pages and the amount of content of the collection folder: {minute} minutes, {second} seconds.")

    # In case you press enter without inputing.
    flag = True
    while flag:
        start_page = input(f"\nPlease input a start page (range: 1~{max_page}), press Enter after inputting: ")
        if start_page != '':
            flag = False
    flag = True
    while flag:
        end_page = input(f"Please input an end page (range: {start_page}~{max_page}), press Enter after inputting: ")
        if end_page != '':
            flag = False        

    # The start_page and end_page you get from input is string, so convert them to integers.
    start_page = int(start_page)
    end_page = int(end_page)

    content_seconds = get_content_cost_time(start_page, end_page, max_page, collection_quantity)
    page_seconds = (end_page - start_page) * 10
    total_seconds = content_seconds + page_seconds
    minute = math.floor(total_seconds / 60)
    second = total_seconds % 60

    print(f"\nStart crawling the content, it is estimated that it will take {minute} minutes and {second} seconds, now you can do something else. Do not close the interface. You can view the percentage progress in this interface, or check the crawled content in C:\\__assets__. After the crawling is completed, there will be a prompt with the words \"Crawling completed.\"...")  

    start_time = time.time()
    collection_title = get_collection_title(url_original)

    global process_indicator
    process_indicator = 0

    real_content_quantity = get_real_content_quantity(start_page, end_page, max_page, collection_quantity)
    print(f"\nThe actual number of crawling: {real_content_quantity}\n")

    process = process_indicator / real_content_quantity * 100
    print("\r%.2f%% completed" %process, end='')
    
    for i in range(start_page, end_page+1):
        url = f"{url_original}?page={str(i)}"
        get_contents(url, collection_title, real_content_quantity)
        time.sleep(10)

    print("\n\nCrawling completed.")
    end_time = time.time()
    cost_time = end_time - start_time
    minute = math.floor(cost_time / 60)
    second = cost_time % 60
    print(f"Time cost of crawling content: {minute} minutes, {second} seconds. Now you can close the interface and view the crawled content in C:\\__assets__\\{collection_title}.")
    input()
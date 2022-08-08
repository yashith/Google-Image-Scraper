from array import array
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64
import sys
from PIL import Image
from io import BytesIO
import requests
options=Options()
options.headless =True
options.add_argument("--start-maximized")
options.add_argument("--log-level=3")
driver= webdriver.Chrome("E:\chromedriver.exe",options=options)

VIEW_MORE_CLASS_NAME="mye4qd"
THUMBNAIL_ANCHOR_CLASS_NAME="wXeWr.islib.nfEiy"
IMAGE_ELEMENT_XPATH='//*[@id="imi"]'


google_url=""
target_dir=""
picindex = 0
linkindex= 0
elements=[]



def getgoogleRef(element):
    driver.switch_to.window(windowlist[0])
    element.click()
    url = element.get_attribute("href")
    return url

def save_file(element):
    global picindex,linkindex
    u=getgoogleRef(element)
    driver.switch_to.window(windowlist[1])
    
    try:
        driver.get(u)
        time.sleep(2)
        image_element = driver.find_element_by_xpath(IMAGE_ELEMENT_XPATH)
        url:str = image_element.get_attribute("src")
        r= requests.get(url)
        name_split:array=url.split('.')
        type=name_split[-1]
        if(type == "jpg" or type == "jpeg"):
            open(target_dir+str(picindex)+'.jpg', 'wb').write(r.content)
        elif(type == "png"):
            open(target_dir+str(picindex)+'.png', 'wb').write(r.content)
        elif(type == "webp"):
            open(target_dir+str(picindex)+'.webp', 'wb').write(r.content)
        elif(type == "gif"):
            open(target_dir+str(picindex)+'.gif', 'wb').write(r.content)
        else:
            open(target_dir+str(picindex)+'.jpg', 'wb').write(r.content)
        print(target_dir+str(picindex)+'.jpg saved')
        picindex += 1
    except:
        try:
            data = url.split(',')[1]
            im = Image.open(BytesIO(base64.b64decode(data)))
            im.save(target_dir+str(picindex)+'.jpg', 'JPEG')
            print(target_dir+str(picindex)+'.jpg saved')
            picindex += 1
        except:
            print("URL Error")
    linkindex += 1
    
def gather_image_element():
    global elements
    scrolls =1
    prev_round_count=0
    break_counter=0
    progress ="-"
    while True:
        
        if(prev_round_count!=len(elements)):
            prev_round_count=len(elements)
            break_counter=0
            progress=progress + "-"
        elif(break_counter>5):
            print('\r',progress,end='')
            sys.stdout.write(f"{prev_round_count} images found")
            break
        else:
            break_counter+=1
            progress=progress + "-"
        
        print('\r',progress,end='')

        
        driver.switch_to.window(windowlist[0])    
        height=1080*scrolls
        driver.execute_script("window.scrollTo(0, "+str(height)+")")
        elements=driver.find_elements_by_class_name(THUMBNAIL_ANCHOR_CLASS_NAME)
        scrolls+=1
        time.sleep(2)
        try:
            more_result = driver.find_element_by_class_name(VIEW_MORE_CLASS_NAME)
            more_result.click()
        except:
            print("")

#Main


driver.get(google_url)
mainwindow = driver.current_window_handle
driver.execute_script(f'window.open("{google_url}", "_blank")')
windowlist = driver.window_handles
elements=driver.find_elements_by_class_name(THUMBNAIL_ANCHOR_CLASS_NAME)
gather_image_element()          

while True:
    driver.switch_to.window(windowlist[0])
    save_file(elements[linkindex])
    if(linkindex==len(elements)):
        print("End of array")
        break



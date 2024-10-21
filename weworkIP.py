import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

#匹配ip地址的正则
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
#获取ip地址的网址列表
ip_urls = ["https://myip.ipip.net", "https://ddns.oray.com/checkip", "https://ip.3322.net","https://4.ipw.cn"]
#当前ip地址
current_ip_address = '192.168.1.1'
#企业微信应用管理地址
wechatUrl=f'https://work.weixin.qq.com/wework_admin/frame#/apps/modApiApp/00000000000'
#登录cookie
cookie_header = ""
#覆盖已填写的IP,设置FALSE则添加新IP到已有IP列表里
overwrite = True
#检测间隔时间,默认30分钟,太久会导致cookie失效
detailsTime = 1800

def OpenEdge():
    print("开始请求企业微信网址")
    # 设置目标 URL 和 Cookie 字符串
    # 解析 Cookie 字符串为字典
    cookies = cookie_header.split(';')

    # 启动 Selenium WebDriver
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')  # 无头模式
    driver = webdriver.Edge(options=options)
    driver.get(wechatUrl)
    time.sleep(1)  
    driver.delete_all_cookies()
    for cookie in cookies:
        name, value = cookie.split('=')
        driver.add_cookie({"name": name, "value": value})
    driver.get(wechatUrl)
    time.sleep(1)
    try:
        driver.find_element(By.CLASS_NAME,'login_stage_title_text')
        print("缓存失效,请重新获取")
    except Exception as e:
        e
    return driver
    
def CheckIP():
    print("获取最新IP地址")
    global current_ip_address
    for url in ip_urls:
        ip_address = get_ip_from_url(url)
        if ip_address != "获取IP失败":
            print(f"IP获取成功: {url}: {ip_address}")
            break
        else:
            print(f"请求网址失败: {url}")
    if ip_address != current_ip_address:
        print("检测到IP变化")
        current_ip_address = ip_address
        return True
    else:
        return False
        

def get_ip_from_url(url):
    try:
        # 发送 GET 请求
        response = requests.get(url)
        
        # 检查响应状态码是否为 200
        if response.status_code == 200:
            # 解析响应 JSON 数据并获取 IP 地址
            ip_address = re.search(ip_pattern, response.text)
            if ip_address:
                return ip_address.group()
            else:
                return "获取IP失败"
        else:
            return "获取IP失败"
    except Exception as e:
        print (f"失败,Error: {e}")
        return "获取IP失败"
        
def ChangeIP():
    try:
        print("请求更改IP地址")
        setip = driver.find_element(By.XPATH,'//div[contains(@class, "app_card_operate") and contains(@class, "js_show_ipConfig_dialog")]')
        setip.click()
        time.sleep(1)
        inputArea = driver.find_element(By.XPATH,'//textarea[@class="js_ipConfig_textarea"]')
        confirm = driver.find_element(By.XPATH,'//a[@class="qui_btn ww_btn ww_btn_Blue js_ipConfig_confirmBtn"]')
        if overwrite:
            inputArea.clear()
            inputArea.send_keys(current_ip_address)
        inputArea.send_keys(f';{current_ip_address}')
        confirm.click()
        time.sleep(1)
        print("更改IP地址成功")
    except Exception as e:
        print(f"更改IP地址失败: {e}")
#初始化浏览器
while True:
    try:
        driver = OpenEdge()
        if CheckIP():
            ChangeIP()
        driver.quit()
        time.sleep(detailsTime)
    except Exception as e:
        print(f"发生错误: {e}")
        time.sleep(5)

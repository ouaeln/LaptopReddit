from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timezone, timedelta
from Functions import SelectGPU, TelegramMonitor
from selenium import webdriver
from asyncio.exceptions import CancelledError
from sqlite3 import OperationalError
import configparser
import random
import time

GPU = '3080'

PriceOfGPU = SelectGPU(GPU)

while True:
    try:
        LinkMonitor = TelegramMonitor(PriceOfGPU)
        if LinkMonitor == None:
            print('No Message Found!')
        else:
            print(LinkMonitor[0])
            ct = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            ct = datetime.strptime(ct, "%Y-%m-%d %H:%M:%S")
            t1 = datetime.strptime(str(LinkMonitor[1]).replace('+00:00', ''), "%Y-%m-%d %H:%M:%S")
            t3 = ct-t1
            if t3 < timedelta(minutes=1):
                ShopURL = LinkMonitor[0]
                print(t3)
                break
    except CancelledError:
        print('found error, continuing')
        continue
    except OperationalError:
        time.sleep(5)
        continue

config = configparser.ConfigParser()
config.read("config.ini")

CardNum = config['Card']['CardNum']
Exp = config['Card']['Exp']
CCV = config['Card']['CCV']
Name = config['Card']['Name']

ShopURL = ShopURL
path = Service("C:\\chromedriver.exe")
options = Options()
options.add_argument("--window-size=1280,800")
options.add_argument(r"--user-data-dir=C:\Users\Ouael\AppData\Local\Google\Chrome\User Data\Default")
driver = webdriver.Chrome(options=options, service=path)
driver.get(ShopURL)

while True:
    try:
        driver.find_element_by_xpath('//button[normalize-space()="Acheter cet article"]').click()
        print('found buy button')
        time.sleep(random.randint(1, 2))
        try:
            WarrantyPopUp = driver.find_element_by_xpath("/html/body/div[4]/div[5]/div/div/div[2]/div[4]/div/div[2]/a").click()
            time.sleep(random.randint(1, 2))
            break
        except NoSuchElementException:
            if driver.current_url == 'https://secure2.ldlc.com/fr-fr/DeliveryPayment':
                break
            elif driver.current_url == ShopURL:
                driver.refresh()
                continue
    except NoSuchElementException:
        driver.refresh()
        continue

CardInput = driver.find_element_by_xpath('/html/body/div[3]/div/div[4]/div[2]/div[1]/div/div/form/div[2]/div/input').send_keys(CardNum)
CardInput = driver.find_element_by_xpath('/html/body/div[3]/div/div[4]/div[2]/div[1]/div/div/form/div[3]/div/input[1]').send_keys(Exp)
CardInput = driver.find_element_by_xpath('/html/body/div[3]/div/div[4]/div[2]/div[1]/div/div/form/div[5]/div/input').send_keys(CCV)
CardInput = driver.find_element_by_xpath('/html/body/div[3]/div/div[4]/div[2]/div[1]/div/div/form/div[4]/div/input').send_keys(Name)
time.sleep(random.randint(1, 2))
driver.find_element_by_xpath('/html/body/div[3]/div/div[4]/div[2]/div[1]/div/div/form/div[8]/div/button').click()

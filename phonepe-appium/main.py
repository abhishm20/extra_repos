# from appium import webdriver
# from appium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from appium.webdriver.common.touch_action import TouchAction
#
# # 8273269061
# desired_caps = {}
# desired_caps['platformName'] = 'android'
# desired_caps['platformVersion'] = '9'
# desired_caps['automationName'] = 'uiautomator2'
# desired_caps['deviceName'] = 'Android Emulator'
# # desired_caps['app'] = '/Users/abhishek/Downloads/com.phonepe.app_2019-10-23.apk'
# desired_caps['noReset'] = True
# desired_caps['appPackage'] = 'com.phonepe.app'
# desired_caps['appActivity'] = 'com.phonepe.app.ui.activity.Navigator_MainActivity'
#
# driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
#
# # store = driver.find_element_by_name("Store")
#
# # store.click()
#
# # driver.quit()
#
# element = driver.find_element_by_id('com.phonepe.app:id/tl_main_page_bottom_tabs')
# print(len(element.find_elements_by_class_name("androidx.appcompat.app.a$c")))
# print(element.find_elements_by_class_name("androidx.appcompat.app.a$c")[1].click())
#
# wait = WebDriverWait(driver, 20)
# currently_waiting_for = wait.until(EC.presence_of_element_located((By.ID, 'com.phonepe.app:id/sd_recycler_view')))
#
# driver.swipe(75, 2000, 75, 300)
#
# for e in driver.find_elements_by_class_name("android.view.ViewGroup"):
#     e.click()
#     driver.find_element_by_id("com.phonepe.app:id/iv_back_icon").click()
#     # break
#     # for a in e.find_elements_by_class_name("android.widget.ImageView"):
#     #     if a.get_attribute('clickable') == "true":
#     #         a.click()
#     #         print(driver.find_element_by_android_uiautomator('new UiSelector().text("Call")'))
#     #
#     #     else:
#     #         print("Not clickable")
from appium import webdriver
from appium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
import csv

# 8273269061
desired_caps = {}
desired_caps['platformName'] = 'android'
desired_caps['platformVersion'] = '9'
desired_caps['automationName'] = 'uiautomator2'
desired_caps['deviceName'] = 'd120ae93'
# desired_caps['app'] = '/Users/ayush/Downloads/com.phonepe.app_2019-10-23.apk'
desired_caps['noReset'] = True
desired_caps['appPackage'] = 'com.phonepe.app'
desired_caps['appActivity'] = 'com.phonepe.app.ui.activity.Navigator_MainActivity'

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
actions = TouchAction(driver)

element = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.ImageView')
element.click()
placeholder = driver.find_element_by_class_name('android.view.View')
placeholder.click()

wait = WebDriverWait(driver, 20)

def storepage(viewnumber=0):
    wait.until(EC.presence_of_element_located((By.ID, 'com.phonepe.app:id/sd_category_filter_rv'))) # Wait for the store page to load
    # Extend the store page
    actions.long_press(x=535, y=2096, duration=30)
    actions.move_to(x=535, y=1641)
    actions.release()
    actions.perform()

    # For Loop takes care of handling the swiping of store pages
    for x in range(0, viewnumber):
        actions.long_press(x=535, y=2054, duration=30)
        actions.move_to(x=535, y=100)
        actions.release()
        actions.perform()

# Sees the page upto which the scraping should happen. n refers to the page number
def crawler(n=0):
    stores = []
    for viewnum in range(0, n):
        print("Page {}".format(viewnum))
        storepage(viewnumber=viewnum)
        i = -1
        while i < 8:
            i = i + 1
            all_elements = driver.find_elements_by_class_name("android.view.ViewGroup")
            all_elements[i].click()
            wait.until(EC.presence_of_element_located((By.ID, 'com.phonepe.app:id/id_store_image')))
            # Responsible for extending the store page
            actions.long_press(x=535, y=2096, duration=3)
            actions.move_to(x=535, y=1641)
            actions.release()
            actions.perform()
            category = None
            address = None
            rating = None
            try:
                category = driver.find_element_by_id('com.phonepe.app:id/tvStoreCategory').text
            except Exception as e:
                pass
            try:
                address = driver.find_element_by_id('com.phonepe.app:id/tvStoreAddr').text
            except Exception as e:
                pass
            try:
                rating = driver.find_element_by_id('com.phonepe.app:id/tvStoreRating').text
            except Exception as e:
                pass
            template_dict = {
                'NAME': driver.find_element_by_id('com.phonepe.app:id/tvStoreName').text,
                'CATEGORY': category,
                'ADDR': address,
                'RATING': rating
            }
            # driver.find_element_by_id('com.phonepe.app:id/llCall').click()
            # template_dict['PHONE'] = driver.find_element_by_id('com.android.dialer:id/digits').text()
            print(template_dict)
            stores.append(template_dict)
            # driver.back()
            driver.back()
            storepage(viewnumber=viewnum)

# Handles conversion of scraped data into CSV

    keys = stores[0].keys()

    with open('mycsvfile.csv', 'w') as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        for store in stores:
            w.writerow(store)


# Add value of n in the crawler() to crawl different view pages.
crawler(n=3)



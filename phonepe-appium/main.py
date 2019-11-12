from appium import webdriver
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction

# 8273269061
desired_caps = {}
desired_caps['platformName'] = 'android'
desired_caps['platformVersion'] = '9'
desired_caps['automationName'] = 'uiautomator2'
desired_caps['deviceName'] = 'Android Emulator'
# desired_caps['app'] = '/Users/abhishek/Downloads/com.phonepe.app_2019-10-23.apk'
desired_caps['noReset'] = True
desired_caps['appPackage'] = 'com.phonepe.app'
desired_caps['appActivity'] = 'com.phonepe.app.ui.activity.Navigator_MainActivity'

driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)

# store = driver.find_element_by_name("Store")

# store.click()

# driver.quit()

element = driver.find_element_by_id('com.phonepe.app:id/tl_main_page_bottom_tabs')
print(len(element.find_elements_by_class_name("androidx.appcompat.app.a$c")))
print(element.find_elements_by_class_name("androidx.appcompat.app.a$c")[1].click())

wait = WebDriverWait(driver, 20)
currently_waiting_for = wait.until(EC.presence_of_element_located((By.ID, 'com.phonepe.app:id/sd_recycler_view')))

driver.swipe(75, 2000, 75, 300)

for e in driver.find_elements_by_class_name("android.view.ViewGroup"):
    e.click()
    driver.find_element_by_id("com.phonepe.app:id/iv_back_icon").click()
    # break
    # for a in e.find_elements_by_class_name("android.widget.ImageView"):
    #     if a.get_attribute('clickable') == "true":
    #         a.click()
    #         print(driver.find_element_by_android_uiautomator('new UiSelector().text("Call")'))
    #
    #     else:
    #         print("Not clickable")
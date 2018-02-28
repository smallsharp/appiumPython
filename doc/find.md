ID定位

# resourceId属性的方法
driver.find_element_by_id('com.lizi.app:id/setting_imageView').click()
#以accessibility_id进行定位，对Android而言，就是content-description属性
driver.find_element_by_accessibility_id('push_button').click()

ClassName 定位
# 定位唯一元素
self.driver.find_element_by_class_name("android.widget.EditText")
# 找到所有android.widget.EditText并定位第一个
self.driver.find_elements_by_class_name("android.widget.EditText")[0]

Name 定位
#根据name进行定位，对于android来说，就是text属性
driver.find_element_by_name(u"登 录").click（）　

Uiautomator 定位
text属性的方法
driver.find_element_by_android_uiautomator('new UiSelector().text("Custom View")').click()         #text
driver.find_element_by_android_uiautomator('new UiSelector().textContains("View")').click()        #textContains
driver.find_element_by_android_uiautomator('new UiSelector().textStartsWith("Custom")').click()    #textStartsWith
driver.find_element_by_android_uiautomator('new UiSelector().textMatches("^Custom.*")').click()    #textMatches

class属性的方法
#className
driver.find_element_by_android_uiautomator('new UiSelector().className("android.widget.TextView").text("Custom View")').click()
#classNameMatches
driver.find_element_by_android_uiautomator('new UiSelector().classNameMatches(".*TextView$").text("Custom View")').click()

resourceId属性的方法
#resourceId
driver.find_element_by_android_uiautomator('new UiSelector().resourceId("android:id/text1")')
#resourceIdMatches
driver.find_element_by_android_uiautomator('new UiSelector().resourceIdMatches(".*id/text1$")')

元素的其他属性
driver.find_element_by_android_uiautomator('new UiSelector().clickable(true).text("Custom View")').click()
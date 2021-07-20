from selenium import webdriver
import os
import time

# Создание профиля
def get_profile():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.dir', os.path.dirname(__file__).replace("/","\\"))
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')
    profile.set_preference('browser.download.manager.useWindow',False)
    profile.set_preference('pdfjs.disabled',True)
    return profile

# Вход в аккаунт
def login():
    driver.get('https://esia.gosuslugi.ru')
    driver.implicitly_wait(10)
    login = driver.find_element_by_id('login')
    login.send_keys('<PUT LOGIN>')
    password = driver.find_element_by_id('password')
    password.send_keys('<PUT PASSWORD>')
    login_btn = driver.find_element_by_id('loginByPwdButton')
    login_btn.click()

# Получение данных пасспорта
def get_and_write_passport():
    try:
        passport = driver.find_element_by_css_selector('div.row:nth-child(7) > div:nth-child(2)').text
        with open("passport.txt","w") as f:
            f.write(passport)
    except:
        print("Паспорт не найден!")
    
# Получение справки о доходах за прошлый год
def get_reference():
    driver.get('https://www.gosuslugi.ru/358549/1/form')
    try:
        driver.find_element_by_css_selector('.close_popup_x').click()
    except:
        pass
    try:
        driver.find_element_by_css_selector("a.close").click()
    except:
        pass
    dropdown = driver.find_element_by_css_selector('.PGU-dropdown-container')
    time.sleep(3)
    dropdown.click()
    
    prev_year = driver.find_element_by_css_selector('li.ng-binding:nth-child(2)')
    prev_year.click()

    submit_btn = driver.find_element_by_css_selector(r'#Form\.NavPanel\.__nextStep > span:nth-child(1)')
    submit_btn.click()
    time.sleep(10)

    while (True):
        try:
            more_files_btn = driver.find_element_by_css_selector('.link-underline')
            more_files_btn.click()
            reference_items = driver.find_elements_by_class_name('file-item')
            index = -1
            for item in reference_items:
                try:
                    item.find_element_by_class_name('PDF')
                    index = reference_items.index(item)
                except:
                    pass
            reference = reference_items[index].find_element_by_tag_name('a')
            reference.click()
            break
        except:
            time.sleep(60)
            driver.refresh()



if (__name__=="__main__"):
    driver = webdriver.Firefox(firefox_profile=get_profile())
    login()
    get_and_write_passport()
    get_reference()
    driver.close()
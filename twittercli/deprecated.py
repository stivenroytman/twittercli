# --- DEPRECATED ---
# Here is where I put all the functions which I no longer use
# but still wish to keep a record of.
# ------------------

def driverInit(userLogin, userPass, headLess=False):
    if headLess:
        opts = options.Options()
        opts.headless = True
        driver = webdriver.Firefox(options=opts)
    else: 
        driver = webdriver.Firefox()
    driver.get('https://www.twitter.com')
    driver.find_element_by_link_text('Log in').click()
    driver.find_element_by_name('session[username_or_email]')\
            .send_keys(userLogin)
    driver.find_element_by_name('session[password]')\
            .send_keys(userPass)
    driver.find_element_by_name('session[password]')\
            .submit()
    sleep(3)
    return driver
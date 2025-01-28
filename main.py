import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from helpers.driver import chrome_driver

from providers.provider import Provider

from dotenv import load_dotenv

from providers.nst import NST
from providers.thestar import TheStar
from providers.malaymail import MalayMail

load_dotenv()

kritik_user = os.getenv('KRITIK_USER')
kritik_pass = os.getenv('KRITIK_PASS')

def main():

    print("Welcome to Kritik Long, Didn't Read(KLDR) developed by @aidilrx04")

    post = input('Enter post url(valid sites now: nst, thestar, malaymail ): ')

    provider: Provider = None

    if (post.startswith('https://www.nst.com.my/')):
        provider = NST(post)
    elif post.startswith('https://www.thestar.com.my/'):
        provider = TheStar(post)
    elif post.startswith('https://www.malaymail.com/'):
        provider = MalayMail(post)
    else:
        print("Invalid post url")
        exit(-1)

    data = provider.get_data()

    driver = chrome_driver()

    login(driver)

    insert_data(driver, data)

    input()

    driver.quit()

    pass

def login(driver):

    login_url = 'https://kritik.com.my/wp-login.php?redirect_to=https%3A%2F%2Fkritik.com.my%2Fwp-admin%2Fpost-new.php&reauth=1'

    driver.get(login_url)
    time.sleep(1)

    user_input = driver.find_element(By.CSS_SELECTOR, '#user_login')
    pass_input = driver.find_element(By.CSS_SELECTOR, '#user_pass')
    login_btn = driver.find_element(By.CSS_SELECTOR, '#wp-submit')

    # send username and password
    user_input.send_keys(kritik_user)
    pass_input.send_keys(kritik_pass)

    login_btn.click()

    pass

def insert_data(driver, data):
    # assume user already redirected to post new page
    time.sleep(2)

    title_input = driver.find_element(By.CSS_SELECTOR, '#title')
    excerpt_input = driver.find_element(By.CSS_SELECTOR, '#excerpt')
    content_input = driver.find_element(By.CSS_SELECTOR, '#content')
    visual_editor_btn = driver.find_element(By.CSS_SELECTOR, '#content-tmce')

    set_image_btn = driver.find_element(By.CSS_SELECTOR, '#set-post-thumbnail')

    print("Inserting title...")
    title_input.send_keys(data.title)
    time.sleep(.5)

    print('Inserting excerpt...')
    excerpt_input.send_keys(data.excerpt)

    time.sleep(.5)
    driver.execute_script("document.querySelector('#content-html').click()")

    time.sleep(.5)
    print('Inserting content...')
    content_input.send_keys(data.content)
    visual_editor_btn.click()

    # get body
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'iframe#content_ifr'))
    content_body = driver.find_element(By.CSS_SELECTOR, '#tinymce.mce-content-body')

    driver.execute_script("""
    var range = document.createRange();
    range.selectNodeContents(arguments[0]);
    var selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    """, content_body)

    driver.switch_to.default_content()

    color_caret_btn = driver.find_element(By.CSS_SELECTOR,
                                          '.mce-widget.mce-btn.mce-splitbtn.mce-colorbutton > :nth-child(2)')
    color_caret_btn.click()

    black_color = driver.find_element(By.CSS_SELECTOR, '[data-mce-color="#000000"]')

    black_color.click()

    time.sleep(1)
    print("Setting tags")
    if data.tags is not None:
        tags_input = driver.find_element(By.CSS_SELECTOR, 'input#new-tag-post_tag')
        add_tags_btn = driver.find_element(By.CSS_SELECTOR, 'input.button.tagadd')

        tags_input.send_keys(data.get_tags())
        # add_tags_btn.click()
        driver.execute_script("arguments[0].click()", add_tags_btn)
    else:
        print("No tags found, skipping")

    print('Setting featured image...')
    # set_image_btn.click()
    driver.execute_script("arguments[0].click()", set_image_btn)
    time.sleep(1)

    set_featured_image_btn = driver.find_element(By.CSS_SELECTOR,
                                                 'button.media-button-select.media-button.button-primary.button-large')
    image_input = driver.find_element(By.CSS_SELECTOR, ' .moxie-shim.moxie-shim-html5 input[type="file"]')

    image_input.send_keys(data.image)

    WebDriverWait(driver, 60).until(
        lambda d: d.find_element(By.CSS_SELECTOR,
                                 'button.media-button-select.media-button.button-primary.button-large').get_attribute(
            'disabled') is None
    )

    set_featured_image_btn.click()
    print('image setted')

if __name__ == '__main__':
    main()
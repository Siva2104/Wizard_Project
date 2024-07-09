import time

from behave import given, when, then
from selenium import webdriver
from selenium.common import NoSuchWindowException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

service = Service(r"C:\Users\SHIVA\Downloads\project\chromedriver-win64\chromedriver-win64\chromedriver.exe")
chrome_browser = webdriver.Chrome(service=service)


def start_browser():
    global chrome_browser
    if chrome_browser:
        chrome_browser.quit()
    chrome_browser = webdriver.Chrome(service=service)


@given('I am on the Demo Login Page')
def step_impl(context):
    chrome_browser.get("https://www.saucedemo.com/")
    chrome_browser.maximize_window()
    WebDriverWait(chrome_browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="user-name"]'))
    )


@when('I fill the account information for account {user} into the Username field and the Password field')
def step_impl(context, user):
    WebDriverWait(chrome_browser, 10).until(
        EC.element_to_be_clickable((By.ID, 'user-name'))
    )
    username_field = chrome_browser.find_element(By.ID, 'user-name')
    password_field = chrome_browser.find_element(By.ID, 'password')

    print(f"Filling in credentials for {user}.")
    if user == 'StandardUser':
        username = 'standard_user'
        password = 'secret_sauce'
    elif user == 'LockedOutUser':
        username = 'locked_out_user'
        password = 'secret_sauce'

    username_field.send_keys(username)
    password_field.send_keys(password)
    print("Credentials filled in.")
    # You may need to wait for elements or perform other actions here


@when('I click the Login Button')
def step_impl(context):
    login_button = chrome_browser.find_element(By.ID, 'login-button')
    login_button.click()


@then(u'I am redirected to the Demo Main Page')
def step_impl(context):
    WebDriverWait(chrome_browser, 10).until(
        EC.url_contains("/inventory.html")
    )
    current_url = chrome_browser.current_url
    assert "/inventory.html" in current_url, f"Expected to be on the inventory page, but was on {current_url}"
    print("Successfully redirected to the Demo Main Page.")


@then(u'I verify the App Logo exists')
def step_impl(context):
    app_logo = WebDriverWait(chrome_browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'app_logo'))
    )
    assert app_logo.is_displayed(), "App logo is not displayed."
    print("App logo is displayed.")


@when(u'user sorts products from low price to high price')
def step_impl(context):
    WebDriverWait(chrome_browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'product_sort_container'))
    )
    sort_dropdown = chrome_browser.find_element(By.CLASS_NAME, 'product_sort_container')
    sort_dropdown.click()
    sort_option = WebDriverWait(chrome_browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="header_container"]/div[2]/div/span/select/option[3]'))
    )
    sort_option.click()
    print("Sorted products from low price to high price.")


@when('user adds lowest priced product')
def step_impl(context):
    add_to_cart_buttons = chrome_browser.find_elements(By.XPATH,
                                                       "//div[@class='pricebar']//button")
    time.sleep(5)
    for button in add_to_cart_buttons[:6]:
        time.sleep(2)
        button.click()
        print("Item added to cart.")


@when('user clicks on cart')
def step_impl(context):
    cart_check = chrome_browser.find_element(By.ID, "shopping_cart_container")
    cart_check.click()
    time.sleep(2)


@when('user clicks on checkout')
def step_impl(context):
    cart_check = chrome_browser.find_element(By.ID, "checkout")
    cart_check.click()
    time.sleep(2)


@when('user enters first name {first_name}')
def step_impl(context, first_name):
    first_name_field = chrome_browser.find_element(By.ID, 'first-name')
    first_name_field.send_keys(first_name)
    print(f"Entered first name: {first_name}")
    time.sleep(5)


@when('user enters last name {last_name}')
def step_impl(context, last_name):
    last_name_field = chrome_browser.find_element(By.ID, 'last-name')
    last_name_field.send_keys(last_name)
    print(f"Entered last name: {last_name}")
    time.sleep(5)


@when('user enters zip code {zip_code}')
def step_impl(context, zip_code):
    zip_code_field = chrome_browser.find_element(By.ID, 'postal-code')
    zip_code_field.send_keys(zip_code)
    print(f"Entered zip code: {zip_code}")
    time.sleep(5)


@when('user clicks Continue button')
def step_impl(context):
    continue_button = chrome_browser.find_element(By.ID, 'continue')
    continue_button.click()
    print("Clicked on Continue button.")
    time.sleep(5)


@then('I verify in Checkout overview page if the total amount for the added item is ${total_amount}')
def step_impl(context, total_amount):
    total_amount_element = WebDriverWait(chrome_browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'summary_total_label'))
    )
    assert total_amount in total_amount_element.text, f"Expected total amount {total_amount}, but got {total_amount_element.text}"
    print(f"Verified total amount: {total_amount}")
    time.sleep(10)


@when('user clicks Finish button')
def step_impl(context):
    finish_button = chrome_browser.find_element(By.ID, 'finish')
    finish_button.click()
    print("Clicked on Finish button.")


@then('Thank You header is shown in Checkout Complete page')
def step_impl(context):
    thank_you_header = WebDriverWait(chrome_browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'complete-header'))
    )
    assert thank_you_header.text == "THANK YOU FOR YOUR ORDER", "Thank You header not found"
    print("Verified 'Thank You' header in Checkout Complete page.")


def after_scenario(context, scenario):
    if chrome_browser:
        chrome_browser.quit()
    print("Closed the browser after the scenario.")

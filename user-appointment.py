import time
import pytest

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, ElementNotInteractableException


@pytest.fixture
def firefox_driver():
    """
        setup web driver
    """
    # service = Service('geckodriver')
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(options=options)
    yield driver
    time.sleep(5)
    driver.quit()


def wait_for_element(driver, by, value, timeout=2, poll_frequency=0.2):
    """
        wait until element is found
        :param driver: Selenium WebDriver instance
        :param by: element locator type
        :param value: element location path
        :param timeout: waiting time
        :param poll_frequency: frequency time to check the element
    """
    errors = [NoSuchElementException, ElementNotInteractableException]    
    wait = WebDriverWait(driver, timeout=timeout, poll_frequency=poll_frequency, ignored_exceptions=errors)
    return wait.until(lambda d : d.find_element(by, value))

def perform_mouse_click_action(driver: webdriver, by, value):
    """
        Perform muse actions
        :param driver: Selenium WebDriver instance
        :param by: element locator type
        :param value: element location path
    """
    element = driver.find_element(by, value)
    ActionChains(driver)\
        .click(element)\
        .perform()
    
def select_date(driver: webdriver):
    """
        Select a date in the date picker widget.
        :param driver: Selenium WebDriver instance
    """
    # click on date input field
    perform_mouse_click_action(driver, By.CLASS_NAME, 'input-group-addon')
    
    # Move to month list 
    perform_mouse_click_action(driver, By.CLASS_NAME, 'datepicker-switch')
    
    # Move to year list
    perform_mouse_click_action(driver, By.CSS_SELECTOR, 'div.datepicker-months > table > thead > tr > th.datepicker-switch')
    
    # Select year from year list
    perform_mouse_click_action(driver, By.XPATH, '/html/body/div/div[3]/table/tbody/tr/td/span[7]')
    
    # Select month from month list
    perform_mouse_click_action(driver, By.CSS_SELECTOR, 'span.month:nth-child(7)')
    
    # Select day from day list
    perform_mouse_click_action(driver, By.XPATH, '/html/body/div/div[1]/table/tbody/tr[5]/td[2]')


def test_make_appointment_navigates_to_login(firefox_driver: webdriver):
    """ Open CURA Healthcare Service web site """
    firefox_driver.get('https://katalon-demo-cura.herokuapp.com/')

    # Find make-appointment button go to login page in not logged in
    appointment_button = wait_for_element(firefox_driver, By.ID, 'btn-make-appointment')
    appointment_button.click()

    """ After reaching login page """
    login_text = wait_for_element(firefox_driver, By.CSS_SELECTOR, 'div.text-center > h2') # Find element by CSS_SELECTOR
    # login_text = wait_for_element(firefox_driver, By.XPATH, '/html/body/section/div/div/div[1]/h2') # Find element by XPATH
    
    assert login_text.text == 'Login', "Expectedtxt_comment 'Login' text not found on the page"

    # Find demon username and password for login
    demo_username = firefox_driver.find_element(By.XPATH, '/html/body/section/div/div/div[2]/form/div[1]/div[1]/div/div/input')
    demo_password = firefox_driver.find_element(By.XPATH, '/html/body/section/div/div/div[2]/form/div[1]/div[2]/div/div/input')

    assert demo_username.get_attribute('value') == 'John Doe', "Expected 'John Doe' text not found on the page"
    assert demo_password.get_attribute('value') == 'ThisIsNotAPassword',  "Expected 'ThisIsNotAPassword' text not found on the page"

    # Find input element set key to input field
    username = firefox_driver.find_element(By.ID, 'txt-username')
    password = firefox_driver.find_element(By.ID, 'txt-password')
    submit_button = firefox_driver.find_element(By.ID, 'btn-login')

    # set username and password in input element and click to login button for login
    username.send_keys(demo_username.get_attribute('value'))
    password.send_keys(demo_password.get_attribute('value'))
    submit_button.click()
    
    make_appointment_text = wait_for_element(firefox_driver, By.CSS_SELECTOR, 'div.text-center > h2')
    assert make_appointment_text.text == 'Make Appointment', "Expected 'Make Appointment' is not  found on the page"

    """After success fully logged in Create an appointment."""
    # Find facility element and select second item from dropdown
    facility_element = firefox_driver.find_element(By.ID, 'combo_facility')
    select = Select(facility_element)
    select.select_by_index(1)

    # Handle checkbox element
    check_permission = firefox_driver.find_element(By.ID, 'chk_hospotal_readmission')
    check_permission.click()

    # Handle radio check element
    healthcare_program = firefox_driver.find_element(By.XPATH, "//input[@id='radio_program_medicaid' and @name='programs' and @value='Medicaid']")
    healthcare_program.click()

    # Handle Date Field
    select_date(firefox_driver)

    # Add comments
    comment_field = firefox_driver.find_element(By.ID, 'txt_comment')
    comment_field.send_keys(" \
        আপনি যখন করবেন আমার ওপেন হার্ট সার্জারি, \
        দেখবেন হার্টের মাঝখানে \
        একটা মেয়ে রূপসী ভারি, \
        আপনি যখন করবেন আমার ওপেন হার্ট সার্জারি, \
        দেখবেন হার্টের মাঝখানে \
        একটা মেয়ে রুপসী ভারি \
        ছুরি কাঁচি সুঁইয়ের \
        খোঁচা তার যেন না লাগে, \
        আমার বাঁচা মরা পরে, \
        তার জীবনটা আগে গো ডাক্তার, \
        ও ডাক্তার.. \
    ")

    # Book appointment
    firefox_driver.find_element(By.ID, 'btn-book-appointment').click()


    """ go to history page to see appointment booking list """
    # Open menu list
    firefox_driver.find_element(By.ID, 'menu-toggle').click()

    # Go to appointment history page
    firefox_driver.find_element(By.CSS_SELECTOR, '.sidebar-nav > li:nth-child(4) > a:nth-child(1)').click()


# .sidebar-nav > li:nth-child(4) > a:nth-child(1)

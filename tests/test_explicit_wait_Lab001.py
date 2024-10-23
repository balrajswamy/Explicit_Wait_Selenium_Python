import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (ElementNotVisibleException, ElementNotSelectableException, TimeoutException)
import allure
import time


@allure.title("TestCase #1 to test an explicit wait at https://app.vwo.com")
@allure.description("Verify the invalid username/email with password")
@allure.step("Verify the username with password and getting an error message")
@allure.step("Checking invalid login using wrong input username|password")
@pytest.mark.smoke
def test_invalid_login():
    # Initialize WebDriver and maximize the window
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Navigate to the login page
        driver.get("https://app.vwo.com/#/login")

        email_input_wait = WebDriverWait(driver = driver, poll_frequency=1,timeout=5,
                             ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,
                                                 TimeoutException])

        # Waiting to Locate email field and input email to become visible
        email_input = email_input_wait.until(
            EC.visibility_of_element_located((By.XPATH, '//input[@name="username"]'))        )
        email_input.send_keys("balraj@gmail.com")
        time.sleep(1)

        # Locate password field and input password
        password = driver.find_element(By.XPATH, "//input[@name='password']")
        password.send_keys("123@123")
        time.sleep(1)

        # Click on the login button
        driver.find_element(By.XPATH, '//button[@id="js-login-btn"]').click()


        # Fluent wait: wait for the error message to appear
        wait = WebDriverWait(driver = driver, poll_frequency=1,timeout=5,
                             ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,
                                                 TimeoutException])

        # Waiting for the error message to become visible
        error_message_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="js-notification-box-msg"]'))
        )

        # Extract the text from the error message
        error_message = error_message_element.text
        print("error_message:\t", error_message)
        # Assertion: Check if the error message matches the expected text
        assert 'Your email, password, IP address or location did not match' in error_message, \
            f"Expected error message not found! Got: {error_message}"

    except TimeoutException:
        # If the element isn't found within the time, the test will fail
        assert False, "Error message was not displayed in time"

    finally:
        # Close the browser after the test completes
        driver.quit()

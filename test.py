import os
import random
import time

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@allure.feature("DemoQA Form Submission")
@allure.story("Заполнение и отправка формы")
def test_form_submission(driver):
    with allure.step("Открыть страницу регистрации"):
        driver.get('https://demoqa.com/automation-practice-form')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'firstName'))
        )

    with allure.step("Заполнить поле First Name"):
        first_name_input = driver.find_element(By.ID, 'firstName')
        first_name_input.send_keys('Иван')

    with allure.step("Заполнить поле Last Name"):
        last_name_input = driver.find_element(By.ID, 'lastName')
        last_name_input.send_keys('Иванов')

    with allure.step("Заполнить поле Email"):
        email_input = driver.find_element(By.ID, 'userEmail')
        email_input.send_keys('ivanov@example.com')

    with allure.step("Выбрать пол"):
        gender_radio = driver.find_element(By.XPATH, "//label[contains(text(), 'Male')]")
        gender_radio.click()

    with allure.step("Заполнить поле Mobile"):
        mobile_input = driver.find_element(By.ID, 'userNumber')
        mobile_input.send_keys(''.join([str(random.randint(0, 9)) for _ in range(10)]))

    with allure.step("Заполнить поле Date of Birth"):
        dob_input = driver.find_element(By.ID, 'dateOfBirthInput')
        dob_input = driver.find_element(By.ID, 'dateOfBirthInput')
        driver.execute_script("arguments[0].scrollIntoView();", dob_input)
        dob_input.click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'react-datepicker__month-select'))
        ).send_keys('January')
        driver.find_element(By.CLASS_NAME, 'react-datepicker__year-select').send_keys('1990')
        day = driver.find_element(By.XPATH, "//div[contains(@class, 'react-datepicker__day') and text()='15']")
        day.click()

    with allure.step("Заполнить поле Subjects"):
        subjects_input = driver.find_element(By.ID, 'subjectsInput')
        subjects_input.send_keys('Maths')
        subjects_input.send_keys(Keys.RETURN)

    with allure.step("Загрузить изображение"):
        picture_input = driver.find_element(By.ID, 'uploadPicture')
        current_directory = os.path.dirname(os.path.abspath(__file__))
        picture_path = os.path.join(current_directory, 'example.jpg')

        if os.path.isfile(picture_path):
            picture_input.send_keys(picture_path)
        else:
            allure.attach(f"Файл {picture_path} не найден.", name="Файл не найден", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Заполнить поле Current Address"):
        current_address_input = driver.find_element(By.ID, 'currentAddress')
        current_address_input.send_keys('ул. Примерная, д. 1, кв. 1')

    with allure.step("Выбрать штат"):
        state_dropdown = driver.find_element(By.ID, 'react-select-3-input')
        state_dropdown.send_keys('NCR')
        time.sleep(1)
        state_dropdown.send_keys(Keys.RETURN)

    with allure.step("Выбрать город"):
        city_dropdown = driver.find_element(By.ID, 'react-select-4-input')
        city_dropdown.send_keys('Delhi')
        time.sleep(1)
        city_dropdown.send_keys(Keys.RETURN)

    with allure.step("Нажать кнопку Submit"):
        submit_button = driver.find_element(By.ID, 'submit')
        submit_button.click()

    with allure.step("Проверка успешной отправки формы"):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'example-modal-sizes-title-lg'))
        )

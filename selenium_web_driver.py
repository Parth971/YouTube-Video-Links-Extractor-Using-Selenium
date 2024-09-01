from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable,
    presence_of_element_located,
)
import undetected_chromedriver as uc


class SeleniumWebDriverManager:
    wait = 10

    def get_options(self, headless: bool = False):
        options = uc.ChromeOptions()

        if headless:
            options.add_argument("--headless")
        else:
            options.add_argument("--start-maximized")

        return options

    @property
    def web_driver_wait(self):
        return WebDriverWait(self, self.wait)

    def web_driver_wait_till_existence(self, by: str, value: str):
        return self.web_driver_wait.until(presence_of_element_located((by, value)))

    def web_driver_wait_and_click(self, by: str, value: str):
        element = self.web_driver_wait.until(element_to_be_clickable((by, value)))
        element.click()

    def web_driver_wait_and_send_inputs(self, by: str, value: str, input_text: str):
        element = self.web_driver_wait.until(element_to_be_clickable((by, value)))
        element.send_keys(input_text)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumWebDriver:
    """
    Wrapper class for initializing and managing a Selenium WebDriver instance.

    Properties:
        web_driver_wait (WebDriverWait): Returns a WebDriverWait instance with the specified wait time.
        web_driver (webdriver.Chrome): Returns the Selenium WebDriver instance.

    Attributes:
        _driver: The internal reference to the Selenium WebDriver instance.
        wait (int): The default wait time in seconds for WebDriverWait.

    """
    def __init__(self):
        self._driver = None
        self.wait = 10

    @property
    def web_driver_wait(self):
        """
        Returns a WebDriverWait instance with the specified wait time.

        Returns:
            WebDriverWait: An instance of WebDriverWait.

        """
        return WebDriverWait(self.web_driver, self.wait)

    @property
    def web_driver(self) -> webdriver.Chrome:
        """
        Returns the Selenium WebDriver instance.

        Returns:
            webdriver.Chrome: The Selenium WebDriver instance.

        """
        if self._driver is not None:
            return self._driver

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        self._driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        return self._driver

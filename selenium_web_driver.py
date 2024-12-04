from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver


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

    def __init__(self) -> None:
        self._driver: Optional[webdriver.Chrome] = None
        self.wait = 10

    @property
    def web_driver_wait(self) -> WebDriverWait[WebDriver]:
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
        # options.add_argument("--headless=new")
        # options.add_argument("--start-maximized")

        self._driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

        if self._driver is None:
            raise Exception("Unable to create webdriver")

        return self._driver

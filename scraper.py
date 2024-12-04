import contextlib
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from twocaptcha import TwoCaptcha

from undetected_chromedriver import Chrome

from selenium_web_driver import SeleniumWebDriverManager
from utils import handle_exception, calc_time


class YoutubeDetailsScraper(SeleniumWebDriverManager, Chrome):
    debug = True
    data_sitekey = "6Lf39AMTAAAAALPbLZdcrWDa8Ygmgk_fmGmrlRog"
    _2CAPTCHA_API_KEY = "e0203754234a625b5424a1594081f8b5"

    def __init__(self):
        self.solver = TwoCaptcha(self._2CAPTCHA_API_KEY)
        super().__init__(options=self.get_options(headless=False))
        self.is_logged_in = False
        self.result = {}

    def __del__(self):
        self.quit()

    @calc_time
    def open_link(self, link):
        self.get(url=link)

    @calc_time
    def extract_details(self) -> dict:
        self.web_driver_wait_and_click(
            by=By.CSS_SELECTOR,
            value="yt-description-preview-view-model truncated-text > button",
        )

        have_email = False
        with contextlib.suppress(Exception):
            self.web_driver_wait_and_click(
                by=By.XPATH,
                value="//button[.//span[text()='View email address']]",
            )
            element = self.web_driver_wait_till_existence(
                by=By.XPATH,
                value="//iframe[@title='reCAPTCHA']",
            )
            captcha_page_url = element.get_attribute("src")
            breakpoint()
            try:
                response = self.solver.recaptcha(
                    sitekey=self.data_sitekey, url=captcha_page_url
                )
                code = response["code"]
                print(code)

                recaptcha_response_element = self.find_element(
                    By.ID, "g-recaptcha-response"
                )
                self.execute_script(
                    f'arguments[0].value = "{code}";', recaptcha_response_element
                )
            except Exception as e:
                breakpoint()
                print(e)
                print("Captcha not solved")

            self.web_driver_wait_and_click(by=By.ID, value="submit-btn")
            have_email = True

        element = self.web_driver_wait_till_existence(
            by=By.XPATH,
            value="//*[@id='additional-info-container']/table",
        )

        try:
            return self.get_info(
                html=element.get_attribute("outerHTML"),
                have_email=have_email,
            )
        except Exception:
            return {"email": None, "location": None}

    def get_info(self, html: str, have_email: bool) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        information = []
        for tr in soup.find_all("tr"):
            tds = tr.find_all("td")
            if tds:
                val = tds[-1].text.strip()
                if val:
                    information.append(val)

        return {
            "email": information[0] if have_email else None,
            "location": information[-1],
        }

    def login(self):
        if not self.is_logged_in:
            self.web_driver_wait_and_click(
                by=By.CSS_SELECTOR,
                value="#end ytd-button-renderer a",
            )
            self.web_driver_wait_and_send_inputs(
                by=By.ID,
                value="identifierId",
                input_text="desaiparth974@gmail.com",
            )

            self.web_driver_wait_and_click(
                by=By.CSS_SELECTOR,
                value="#identifierNext button",
            )

            self.web_driver_wait_and_send_inputs(
                by=By.NAME,
                value="Passwd",
                input_text="Parth@2000",
            )

            self.web_driver_wait_and_click(
                by=By.CSS_SELECTOR,
                value="#passwordNext button",
            )

            input("Press Enter key after authentication complete...")
            self.is_logged_in = True

    @handle_exception
    @calc_time
    def scrap(self, yt_channel_link):
        print(f"Scraping link: {yt_channel_link}")

        self.open_link(link=yt_channel_link)

        if len(self.window_handles) > 1:
            for window_handle in self.window_handles[:-1]:
                self.switch_to.window(window_handle)
                self.close()

        self.login()

        details = self.extract_details()

        self.result[yt_channel_link] = details
        print(f"Link {yt_channel_link} details: {details}")


if __name__ == "__main__":
    links = [
        "https://www.youtube.com/@TradingLabOfficial",
        "https://www.youtube.com/@cosdensolutions",
        "https://www.youtube.com/@MikeShake",
        "https://www.youtube.com/@TropicalMage-kn6se",
        "https://www.youtube.com/@Fireship",
        "https://www.youtube.com/@TechBurner",
    ]

    youtube_details_scraper = YoutubeDetailsScraper()

    for link in links:
        youtube_details_scraper.scrap(link)

    print(youtube_details_scraper.result)

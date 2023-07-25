import pathlib
import time
from bs4 import BeautifulSoup
import json

from selenium_web_driver import SeleniumWebDriver
from selenium.webdriver.common.by import By

from utils import handle_exception, calc_time


class YoutubeScraper(SeleniumWebDriver):
    """
    A class for scraping YouTube videos from a specific channel using Selenium WebDriver.

    Attributes:
        domain (str): The base domain for YouTube.
        loading_time_limit (int): The wait time in seconds for new content to load.
        debug (bool): Flag indicating whether to enable debug mode.

    """
    domain = 'https://www.youtube.com'
    loading_time_limit = 2  # Wait for new content to load (in seconds)
    debug = True

    def __init__(self):
        super(YoutubeScraper, self).__init__()

    def scroll(self, target_height):
        """
        Scroll the web page to a specific height.

        Args:
            target_height (int): The target height to scroll to.

        """
        self.web_driver.execute_script(f"window.scrollTo(0, {target_height});")

    @calc_time
    def scroll_till_end(self):
        """
        Scroll the web page until reaching the end.

        This method scrolls the page to the bottom and waits for new content to load,
        repeating the process until no new content is loaded.

        """
        previous_height = 0
        counter = 1

        while True:
            height = self.web_driver.execute_script(
                "return document.documentElement.scrollHeight;")

            self.scroll(target_height=height)

            print(f'Loading new videos ({counter})...')

            start_time = time.time()
            while True:
                new_height = self.web_driver.execute_script(
                    "return document.documentElement.scrollHeight;")

                if height != new_height:
                    break

                end_time = time.time()

                if end_time - start_time > self.loading_time_limit:
                    break

            if previous_height == height:
                print('\nLoaded all videos')
                break

            previous_height = height
            counter += 1

    @calc_time
    def extract_links(self):
        """
        Extract video links from the loaded web page.

        Returns:
            list: A list of extracted video links.

        """
        html = self.web_driver.find_element(By.XPATH, 'html').get_attribute('innerHTML')
        text = f"<html>{html}</html>"

        self.web_driver.quit()

        soup = BeautifulSoup(text, "html.parser")
        links_xpath = 'div#contents ytd-rich-grid-row ytd-rich-item-renderer ytd-thumbnail a#thumbnail'
        elements = soup.select(links_xpath)
        print("soup.select('div#contents ytd-rich-grid-row')", len(soup.select('div#contents ytd-rich-grid-row')))
        print(len(elements))
        return [
            element.attrs.get('href').split('=')[-1]
            for element in elements
        ]

    @calc_time
    def save_links(self, links):
        """
        Save the extracted video links to a JSON file.

        Args:
            links (list): A list of video links to be saved.

        """
        with open(BASE_DIR / 'links1.json', 'w') as fp:
            json.dump(links, fp)

    @calc_time
    def open_link(self, link):
        """
        Open a specified link in the web driver.

        Args:
            link (str): The link to be opened.

        """
        self.web_driver.get(url=link)

    @handle_exception
    @calc_time
    def scrap(self, yt_channel_name):
        """
        Scrape videos from a YouTube channel.

        Args:
            yt_channel_name (str): The name of the YouTube channel.

        """
        link = f"{self.domain}/@{yt_channel_name}/videos"
        link = f"{self.domain}/@{yt_channel_name}/videos"

        print(f'Scraping link: {link}')

        # Open Youtube channel page
        self.open_link(link=link)

        # Scroll till end
        self.scroll_till_end()

        # Extract all links
        print('Extracting links...')
        video_links = self.extract_links()

        print('Saving Links...')
        self.save_links(video_links)


if __name__ == '__main__':
    """
    Entry point of the script.

    Scrapes videos from a specific YouTube channel.

    Environment Variables:
        YOUTUBE_API_KEY (str): The API key for accessing the YouTube Data API.

    Prints:
        A completion message after the scraping process.

    """

    BASE_DIR = pathlib.Path(__file__).parent.resolve()
    channel_name = 'thenewboston'

    youtube_scraper = YoutubeScraper()
    youtube_scraper.scrap(yt_channel_name=channel_name)
    
    print(f'{"#"*10} Completed {"#"*10}')

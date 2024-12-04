import pathlib
import time
from typing import List
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

    domain = "https://www.youtube.com"
    loading_time_limit = 2  # Wait for new content to load (in seconds)
    debug = True

    def __init__(self) -> None:
        super(YoutubeScraper, self).__init__()

    def scroll(self, target_height: int) -> None:
        """
        Scroll the web page to a specific height.

        Args:
            target_height (int): The target height to scroll to.

        """
        self.web_driver.execute_script(f"window.scrollTo(0, {target_height});")  # type: ignore

    @calc_time
    def scroll_till_end(self) -> None:
        """
        Scroll the web page until reaching the end.

        This method scrolls the page to the bottom and waits for new content to load,
        repeating the process until no new content is loaded.

        """
        previous_height = 0
        counter = 1

        while True:
            height = self.web_driver.execute_script(
                "return document.documentElement.scrollHeight;"
            )  # type: ignore

            self.scroll(target_height=height)

            print(f"Loading new videos ({counter})...")

            start_time = time.time()
            while True:
                new_height = self.web_driver.execute_script(
                    "return document.documentElement.scrollHeight;"
                )  # type: ignore

                if height != new_height:
                    break

                end_time = time.time()

                if end_time - start_time > self.loading_time_limit:
                    break

            if previous_height == height:
                print("\nLoaded all videos")
                break

            previous_height = height
            counter += 1

    @calc_time
    def extract_links(self) -> List[str]:
        """
        Extract video links from the loaded web page.

        Returns:
            list: A list of extracted video links.

        """
        # Locate elements directly using Selenium
        elements = self.web_driver.find_elements(
            By.CSS_SELECTOR, "ytd-browse #contents ytd-rich-item-renderer a#thumbnail"
        )

        # Extract video IDs and construct YouTube links
        video_ids = set()
        for element in elements:
            href = element.get_attribute("href")
            if href:
                video_ids.add(href.split("=")[-1])

        links = [
            f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids
        ]

        return links

        # html = self.web_driver.find_element(By.XPATH, "html").get_attribute("innerHTML")
        # text = f"<html>{html}</html>"

        # soup = BeautifulSoup(text, "html.parser")
        # links_xpath = "ytd-browse #contents ytd-rich-item-renderer a#thumbnail"
        # elements = soup.select(links_xpath)

        # extracted_video_ids = [
        #     element.attrs.get("href").split("=")[-1] for element in elements
        # ]
        # video_ids = list(set(extracted_video_ids))

        # links = [
        #     f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids
        # ]

        # return links

    @calc_time
    def save_links(self, channel_name: str, links: List[str]) -> None:
        """
        Save the extracted video links to a JSON file.

        Args:
            links (list): A list of video links to be saved.

        """
        filepath = BASE_DIR / f"output/{channel_name}_links.json"

        # If directory does not exist, create it
        if not filepath.parent.exists():
            filepath.parent.mkdir(parents=True)

        with open(filepath, "w") as fp:
            json.dump(links, fp, indent=4)

    @calc_time
    def open_link(self, link: str) -> None:
        """
        Open a specified link in the web driver.

        Args:
            link (str): The link to be opened.

        """
        opened_tabs = self.web_driver.window_handles
        if len(opened_tabs) > 1:
            for tab in opened_tabs[1:]:
                self.web_driver.switch_to.window(tab)
                self.web_driver.close()
        self.web_driver.get(url=link)

    @handle_exception
    @calc_time
    def scrap(self, yt_channel_name: str) -> None:
        """
        Scrape videos from a YouTube channel.

        Args:
            yt_channel_name (str): The name of the YouTube channel.

        """
        link = f"{self.domain}/@{yt_channel_name}/videos"

        print(f"Scraping link: {link}")

        # Open Youtube channel page
        self.open_link(link=link)

        # Scroll till end
        self.scroll_till_end()

        # Extract all links
        print("Extracting links...")
        video_links = self.extract_links()

        print("Saving Links...")
        self.save_links(yt_channel_name, video_links)


if __name__ == "__main__":
    """
    Entry point of the script.

    Scrapes videos from a specific YouTube channel.

    Environment Variables:
        YOUTUBE_API_KEY (str): The API key for accessing the YouTube Data API.

    Prints:
        A completion message after the scraping process.

    """

    BASE_DIR = pathlib.Path(__file__).parent.resolve()

    channels = [
        "visualizersclub",
        "Skymography",
        "PrakharEditz-yt",
        "manishpathakhere",
    ]

    youtube_scraper = YoutubeScraper()
    for channel in channels:
        youtube_scraper.scrap(yt_channel_name=channel)

    print(f'{"#"*10} Completed {"#"*10}')

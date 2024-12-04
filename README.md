# YouTube Video Links Extractor Using Selenium
It is a tool that takes the name of a YouTube channel as input and uses Selenium, a web automation library, to extract all video links from that channel. The tool then generates a JSON file containing all the video links for easy access and further analysis. This solution is useful for obtaining video data programmatically from YouTube channels without the need for an API key, making it accessible for researchers, content creators, and data enthusiasts.

## Install Virtual Environment

Installing Python (3.11) pakages in virtual environment is recommended.

Install [Python Virtual Environment](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)


## Install requirements.txt

After your virtual environment is activated, run command

    pip install -r requirements.txt


## To Run YouTube Scraper

    python scraper.py

#### Note: To add channel name, open `scraper.py` file, scroll to the bottom of file and change value of variable

    channels = [
        "visualizersclub", 
        "Skymography",
    ] # Name of @channels

After scraper run successfully, their will be files generated named at `output/<channels_name>_links.json` which contains all the videos link.

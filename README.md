# Google Images Downloader

Downloads full quality images from Google. Scrapes image urls and parallel downloads them.

**Prerequisite**: [chromedriver](https://developer.chrome.com/docs/chromedriver/downloads) is required. Put chromedriver in the same directory. The chromedriver version must match the Chrome's version.

## Dependencies
- `selenium`
- `requests`

## To run
1. Install dependencies using `python -m pip install selenium requests`
2. `python downloader.py "search term"`
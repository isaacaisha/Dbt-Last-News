from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.parse
from datetime import datetime
import shutil


def find_chrome_binary_path():
    # Check if Google Chrome is installed
    chrome_path = shutil.which('google-chrome')
    if chrome_path:
        return chrome_path

    # Check if Chromium is installed
    chromium_path = shutil.which('chromium-browser')
    if chromium_path:
        return chromium_path

    return None


app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    # Get the path to the Chrome binary
    chrome_binary_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

    if chrome_binary_path:
        print(f"Found Chrome binary at: {chrome_binary_path}")
    else:
        print("Chrome binary not found.")

    chrome_options = webdriver.ChromeOptions()
    if chrome_binary_path:
        chrome_options.binary_location = chrome_binary_path
    chrome_options.add_argument('--headless')

    # Initialize the ChromeDriver with options and executable path
    driver = webdriver.Chrome(options=chrome_options)

    # Open a website
    driver.get("https://edition.cnn.com/")

    # Wait for a few seconds to ensure the page is loaded
    driver.implicitly_wait(5)

    # Get the page source using Selenium
    page_source = driver.page_source

    # Use Beautiful Soup to parse the page source
    soup = BeautifulSoup(page_source, "html.parser")

    # Find all news headline title elements by their CSS selector
    news_headline_titles = soup.select("div > div > div > a > div > div > span")

    # Extract headline titles and links into a list of dictionaries
    headline_data = []
    base_url = 'https://edition.cnn.com/'  # Define the base URL
    for title_element in news_headline_titles:
        title_text = title_element.get_text()
        parent_element = title_element.find_parent("a")
        if parent_element:
            link = urllib.parse.urljoin(base_url, parent_element.get("href"))  # Join base URL with link
            headline_data.append({"title": title_text, "link": link})

    # Close the web browser
    driver.quit()

    # Render the HTML template with the headline data
    return render_template('index.html', headline_data=headline_data,
                           date=datetime.now().strftime("%a %d %B %Y"))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import chromedriver_autoinstaller
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
import os

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    # Set Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')  # Use the Heroku-provided Chrome binary


    # Use chromedriver_autoinstaller to ensure you have the correct ChromeDriver version
    chromedriver_autoinstaller.install()

    # Initialize the ChromeDriver with options and executable path
    driver = webdriver.Chrome(options=chrome_options)

    # Open a website
    driver.get("https://edition.cnn.com/")

    # Wait for a few seconds to ensure the page is loaded
    driver.implicitly_wait(91)

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
            link = urllib.parse.urljoin(base_url, parent_element.get("href"))  # Join base URL with a link
            headline_data.append({"title": title_text, "link": link})

    # Close the web browser
    driver.quit()

    # Render the HTML template with the headline data
    return render_template('index.html', headline_data=headline_data,
                           date=datetime.now().strftime("%a %d %B %Y"))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

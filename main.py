from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.parse  # Import urllib.parse for URL joining
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    # Initialize the web driver (use an appropriate driver path)
    driver = webdriver.Chrome()

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

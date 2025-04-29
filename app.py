import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary  # noqa: registers chromedriver in PATH
from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "<p>Self-Made Image Location API</p>"

@app.route('/api', methods=['POST'])
def location_data():
    data = request.get_json() or {}
    place = data.get('location')
    if not place:
        return jsonify({'error': 'Missing "location"'}), 400

    url = f'https://unsplash.com/s/photos/{place}'
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    links = [img['src'] for img in soup.find_all('img')
             if img.get('alt') and not img['alt'].startswith('Go to')]
    return jsonify({'links': links})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


# The download_image function is commented out as it's not being used for now.
# def download_image(url, photo_no):
#     # Create the folder if it doesn't exist
#     folder = "images"
#     if not os.path.exists(folder):
#         os.makedirs(folder)

#     # Download the image
#     response = requests.get(url)

#     if response.status_code == 200:
#         # Save the image in the specified folder
#         with open(f"{folder}/downloaded_image_{photo_no}.jpg", "wb") as file:
#             file.write(response.content)
#         print(f"Image {photo_no} downloaded successfully!")
#     else:
#         print(f"Failed to retrieve image {photo_no}. HTTP status code: {response.status_code}")

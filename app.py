import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from flask import Flask, render_template, redirect, url_for,request,jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p>This is a Self Made Image Location API</p>"

@app.route('/api',methods = ['POST'])
def location_data():
    data = request.get_json()
    place_to_search = data.get('location')
    url = f'https://unsplash.com/s/photos/{place_to_search}'
    place_links = []

    options = Options()
    options.add_argument('--headless')  # Runs Chrome in background
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)

    driver.get(url)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    for link in soup.find_all('img'):
        if link.get('alt') and not link.get('alt').startswith('Go to'):
            place_links.append(link.get('src'))

    driver.quit()
    return jsonify({'links':place_links})



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





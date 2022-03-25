import time
from selenium import webdriver
import requests
from PIL import Image
from io import BytesIO
import os

# This program aims to obtain mass images for the creation of datasets that can 
# be used in training models for machine learning.

image_name = input('Write the name to search images: ')

website_url = 'https://www.flickr.com/'
images_urls = []

def init():
    get_website_data()

    print(len(images_urls))

    save_image_from_url()

# Get the divs with the images in the page's html through the url.

def get_website_data():
    driver = webdriver.Chrome('files\chromedriver.exe')
    driver.get(f'{website_url}search/?text={image_name}')

    for i in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

    divs = driver.find_elements_by_class_name('photo-list-photo-view')

    get_images_urls(divs)

def get_images_urls(images_divs: webdriver.remote.webelement.WebElement):
    for image_div in images_divs:
        if image_div != None:

            # Get background-image: from style attribute

            image_url = f"https:{image_div.get_attribute('style').split('(')[2].replace(')', '').replace(';', '')}".replace('"', '')
            images_urls.append(image_url)

# Save image from url to disk

def save_image_from_url():

    # Create dataset folder

    if not os.path.exists('dataset'):
        os.mkdir('dataset')

    # Create folder to save images

    if not os.path.exists(f'dataset/{image_name}'):
        os.makedirs(f'dataset/{image_name}')

    for image_url in images_urls:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image.save(f'dataset/{image_name}/{str(time.time()).replace(".", "")}.jpg')

def compress_dataset_folder():
    # Convert dataset folder to tgz file

    os.system(f'tar -cvzf dataset.tgz dataset')

init()
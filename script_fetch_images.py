from dotenv import load_dotenv, dotenv_values
import os
import requests
import io
from PIL import Image
import json
import hashlib
import hmac
import base64
import urllib.parse as urlparse

load_dotenv()
API_KEY = os.environ.get("API_KEY")
SECRET = os.environ.get("SECRET")


def sign_url(input_url=None, secret=None):
    """
    https://developers.google.com/maps/digital-signature
    Sign a request URL with a URL signing secret.
    """
    if not input_url or not secret:
        raise Exception("Both input_url and secret are required")

    url = urlparse.urlparse(input_url)
    url_to_sign = url.path + "?" + url.query
    decoded_key = base64.urlsafe_b64decode(secret)
    signature = hmac.new(decoded_key, str.encode(url_to_sign), hashlib.sha1)
    encoded_signature = base64.urlsafe_b64encode(signature.digest())
    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    return original_url + "&signature=" + encoded_signature.decode()

def save_image(latitude, longitude, zoom=19, size="640x640", scale=2, key=API_KEY, secret=SECRET):

    # Construct the URL for satellite tile request
    satellite_url = f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom={zoom}&size={size}&scale={scale}&maptype=satellite&key={key}"
    satellite_url = sign_url(satellite_url, secret)

    response = requests.get(satellite_url)

    # Check the response
    if response.status_code == 200:
        # Save the satellite tile image
        img_name = f'satellite_{latitude}_{longitude}_{zoom}_{scale}.png'
        img_path = img_name
        with open(img_path, 'wb') as file:
            file.write(response.content)
        print(f"Satellite tile image saved as '{img_name}'")
    else:
        print(f"Failed to fetch satellite tile. Status code: {response.status_code}")

def main():
    image_coordinates = [
        (32.8353107,-117.1939721), 
        (32.8353005,-117.1921541),
        (32.835252,-117.1905991),
        (32.8371028,-117.1880858),
        (32.8385846,-117.1869454), #5
        (32.839643,-117.1870219),
        (32.8264453,-117.1832565),
        (32.7844412,-117.1668956),
        (32.7862222,-117.1661486),
        (32.7937215,-117.1754918), #10
        (32.7952621,-117.1754151),
        (32.7950809,-117.1676967),
        (32.7806203,-117.2044161),
        (32.7768463,-117.2016394),
        (32.7760929,-117.1929139), #15
        (32.776029,-117.1959058),
        (32.7667972,-117.1910794),
        (32.7919718,-117.0908485),
        (32.7913077,-117.0900226),
        (32.7965164,-117.0835183),
        (32.7974655,-117.0695503), #20
        (32.7956924,-117.0663954),
        (32.8051316,-117.0219805),
        (32.8063108,-117.0209906),
        (32.8052109,-117.0193553),
        (32.8062484,-117.0119538) #25
    ]

    for coord in image_coordinates:
        save_image(*coord)

if __name__ == "__main__":
    main()
    

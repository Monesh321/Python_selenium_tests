from requests_html import HTMLSession
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import pyppdf.patch_pyppeteer
from urllib.parse import urljoin, urlparse
import pytest

import os


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    # initialize the session
    session = HTMLSession()
    # make the HTTP request and retrieve response
    response = session.get(url)
    # execute Javascript
    response.html.render(timeout=100000)
    # construct the soup parser
    soup = bs(response.html.html, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = ""
        if "hidden" not in img:
            img_url = img.attrs.get("src") or img.attrs.get("data-src")
        if not img_url:
            # if img does not contain src attribute, just skip
            print("Broken image url:", img_url)
            res = requests.get(img_url)
            print(res.status_code)
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        # remove URLs like '/hsts-pixel.gif?c=3.2.5'
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
    print(len(urls))
    return urls


def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    flag = True
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)

    # print(response.status_code)
    if response.status_code == 200:
        print("PASSED, image loaded for:", url, "Response code: " + str(response.status_code))
    else:
        flag = False
        print("FAILED, image broken for:", url, "Response code: " + str(response.status_code))

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True,
                    unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
    return flag


def test_img_main(path):
    url = "https://www.sunlife.ca"
    path = urlparse(url).netloc
    # get all images
    imgs = get_all_images(url)
    for img in imgs:
        # for each img, download it
        download(img, path)


if __name__ == "__main__":
    # def test_scrapes_img():
    #     pytest.main()
    # import argparse
    #
    # parser = argparse.ArgumentParser(description="This script downloads all images from a web page")
    # parser.add_argument("url", help="The URL of the web page you want to download images")
    # parser.add_argument("-p", "--path",
    #                     help="The Directory you want to store your images, default is the domain of URL passed")
    #
    # args = parser.parse_args()
    # url = "https://www.sunlife.ca"
    # # url = args.url
    # path = args.path
    #

    # if not path:
    # if path isn't specified, use the domain name of that url as the folder name

    pytest.main()

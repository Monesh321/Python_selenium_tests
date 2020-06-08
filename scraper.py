import time
import pytest
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def check_for_broken_links(URL):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    time.sleep(4)
    alllinks = driver.find_elements_by_tag_name("a")

    # headers = {'User-Agent': ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) "
    #                           "AppleWebKit/537.36 (KHTML, like Gecko) "
    #                           "Chrome/35.0.1916.47 Safari/537.36")}
    headers = {'Accept': 'text/html'}
    flag = True
    for link in alllinks:
        if "#" not in str(link.get_attribute("href")) and "javascript" not in str(
                link.get_attribute("href")) and "linkedin" not in str(link.get_attribute("href")):
            if link.text != '':
                url = link.get_attribute("href")
                try:
                    # driver.find_elements()
                    statusCode = requests.get(url).status_code
                    if statusCode == 200:
                        print(link.text + ":", url, "PASSED with response code:", statusCode)
                        style = link.value_of_css_property("color")
                        print(style)
                    else:
                        print(link.text + ":", url, "FAILED with response code:", statusCode)
                        flag = False
                except Exception as err:
                    print("Something went wrong: ", err)
    if flag == False:
        print("FAILED")
    else:
        print("PASSED")


def test_check_for_broken_links():
    URL = "https://www.sunlife.co.id/ID?vgnLocale=en_CA"
    check_for_broken_links(URL)


if __name__ == '__main__':
    test_check_for_broken_links()

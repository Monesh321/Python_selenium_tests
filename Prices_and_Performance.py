import time

from selenium import webdriver
import requests
import pytest
from selenium.webdriver import ActionChains


class Prices_and_performance():
    def __init__(self, driver):
        self.driver = driver

    locators = {
        "Products_mega_menu": "//span[@class='nav-item-heading'][contains(text(),'Products')]",
        "Products_mega_menu": "//span[@class='nav-item-heading'][contains(text(),'Products')]",

    }
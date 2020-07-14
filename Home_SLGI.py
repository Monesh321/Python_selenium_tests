import time
from urllib.parse import urljoin, urlparse

import bs4
from selenium import webdriver
import requests
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
import requests_html
from lxml import html

# from requests_html import HTML

homeurl = "https://www.sunlifeglobalinvestments.com/"


class Home():
    def __init__(self, driver):
        self.driver = driver

    locators = {
        "Products_mega_menu": "//span[@class='nav-item-heading'][contains(text(),'Products')]",
        "Prices_and_Performance_mega_menu": "//span[@class='nav-item-heading'][contains(text(),'Prices & Performance')]",
        "Insights_and_Resources_mega_menu": "//span[@class='nav-item-heading'][contains(text(),'Insights & Resources')]",
        "About_us_mega_menu": "//span[@class='nav-item-heading'][contains(text(),'About us')]",
        "mega_menu_links": "//li[contains(@class,'dropdown nav-item open')]//div[contains(@class,'hidden-sm hidden-xs')]//li/a",
        "sign_in": "//a[@id='signinbutton']",
        "close_signin": "//button[@class='close-modal']//span[@class='fa fa-remove collapse-x']",
        "search_btn": "//a[contains(text(),'Search')]",
        "input_searchbox": "//input[@id='q-top']",
        "search_suggestions": "//div[@class='search-autocomplete']",
        "footer_section_1": "//ul[@class='footer-socials']//li//a",
        "footer_section_2": "//div[@class='row global-footer-section2']//ul[@class='list-unstyled']//li//a",
        "active_breadcrumb": "//ol[@class='breadcrumb']//li[@class='active']"

    }

    def is_valid(self, url):
        """
        Checks whether `url` is a valid URL.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def verify_title(self):
        title = self.driver.title
        print(title)
        assert title

    def click_signin_btn(self):
        self.driver.find_element_by_xpath(self.locators["sign_in"]).click()
        self.driver.find_element_by_xpath(self.locators["close_signin"]).click()
        time.sleep(3)

    def verify_megamenu_links(self, menu_name):
        element_to_hover_over = self.driver.find_element_by_xpath(self.locators[menu_name])

        hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
        hover.perform()
        # time.sleep(1)
        links = self.driver.find_elements_by_xpath(self.locators["mega_menu_links"])

        count = 0
        for link in links:
            # if "Products" not in link.text:
            #     element_to_hover_over = self.driver.find_element_by_xpath(self.locators[menu_name])
            #     hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
            #     hover.perform()
            time.sleep(3)
            try:
                print("LINK_TEXT:", link.text)
                if link.get_attribute('href') != None and link.get_attribute('href') != '':
                    if 'javascript' not in link.get_attribute('href') and '#' not in link.get_attribute('href'):
                        url = urljoin(homeurl, link.get_attribute('href'))
                        # print(requests.get(url).status_code)
                        page = requests.get(url)
                        content = html.fromstring(page.content)
                        title = content.findtext('.//title')
                        breadcrumb = content.xpath(self.locators["active_breadcrumb"] + "/span/text()")
                        assert breadcrumb
                        assert title

                        print("TITLE:", title)
                        print("BREADCRUMB:", breadcrumb[0])
                        # soup = bs4.BeautifulSoup(page.content, 'lxml')
                        # time.sleep(4)
                        # breadcrumb = soup.findAll('li', attrs={'class': 'active'})
                        # print(breadcrumb)
            except Exception as err:
                print(count)
                print("something wrong: ", err)
                pytest.fail("Test failed", ":", err, pytrace=False)

            # self.driver.find_element_by_partial_link_text(link.text).click()
            # link.click()
            time.sleep(2)
            count = count + 1
            # self.driver.back()

    def verify_search(self):
        self.driver.find_element_by_xpath(self.locators["search_btn"]).click()
        time.sleep(3)
        self.driver.find_element_by_xpath(self.locators["input_searchbox"]).send_keys("investment")
        time.sleep(4)
        search_text = self.driver.find_element_by_xpath(self.locators["search_suggestions"]).text
        assert search_text
        print(search_text)

    def verify_footer_quicklinks(self, footer_xpath):
        footer_links = self.driver.find_elements_by_xpath(self.locators[footer_xpath])
        # for link in footer_links:
        #     print(link.text)
        count = 0
        for link in footer_links:
            if link.text != "Sign in":
                try:
                    url = link.get_attribute('href')
                    print(url)
                    if not self.is_valid(link.get_attribute('href')):
                        url = urljoin(homeurl, link.get_attribute('href'))
                    page = requests.get(url)
                    print(page.status_code)
                    content = html.fromstring(page.content)
                    title = content.findtext('.//title')
                    breadcrumb = content.xpath(self.locators["active_breadcrumb"] + "/span/text()")
                    assert breadcrumb
                    assert title
                    print("#", count)
                    print("LINK TEXT:", link.text)
                    print("TITLE:", title)
                    print("BREADCRUMB:", breadcrumb[0])
                    print()
                except Exception as err:
                    print("#", count)
                    print("error occurred", link.text, err)
                    pytest.fail("FAILED, something wrong with footer links", pytrace=False)
            count = count + 1

            # link.click()
            # time.sleep(2)
            # self.driver.back()
            # # time.sleep(6)

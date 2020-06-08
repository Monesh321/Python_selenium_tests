import csv
import io
import sys
import time
import pytest
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from seleniumpagefactory.Pagefactory import PageFactory
from urllib.parse import urlparse, urlsplit
from selenium.webdriver.common.action_chains import ActionChains
import os.path

from Tests.Home import Homepage, Child_fund_calculator
from Tests.Img_difference import Img_Comparison
from Tests.scraper import check_for_broken_links

baseurl = "https://www.sunlife.co.id/ID?vgnLocale=en_CA"
testdata_filename = "test_data.csv"


def get_data():
    # Retrieve values from CSV
    with open(testdata_filename) as f:
        data = [(line['expected_breadcrumb'], line['link_locator']) for line in csv.DictReader(f)]
        # print(data)
    return data


def chrome_opt():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument(f"--window-size={1920},{3926}")
    chrome_options.add_argument("--hide-scrollbars")
    return chrome_options


@pytest.fixture(scope='function', autouse=True)
def driver(request):
    opt = chrome_opt()
    driver = webdriver.Chrome(options=opt)
    driver.implicitly_wait(8)
    driver.get(baseurl)

    def driver_teardown():
        print("closing browser")
        driver.close()

    request.addfinalizer(driver_teardown)
    yield driver


@pytest.fixture(scope='function', autouse=True)
def homeObj(driver):
    obj = Homepage(driver)
    yield obj


@pytest.fixture(scope='function', autouse=True)
def fundCalcobj(driver):
    obj = Child_fund_calculator(driver)
    yield obj


# @pytest.mark.usefixtures("driver")
# class Homepage(PageFactory):
#     def __init__(self, driver):
#         super().__init__()
#         self.driver = driver
#
#     locators = {"signinBtn": ('XPATH', "//a[@id='signinbutton']"),
#                 "customerSigninHeader": ('XPATH', "//div[@id='customerSignInHeader']"),
#                 "close_signin_formbar": ('XPATH', "//button[@class='close-modal']"),
#                 "select_a_product": ('XPATH', "//select[@id='select-product']"),
#                 "get_a_quote_btn": ('XPATH', "//input[@id='get-a-quote-btn']"),
#                 "life_moments": (
#                     'XPATH', "//a[contains(@class,'dropdown-toggle subnav-trigger')][contains(text(),'Life Moments')]"),
#                 "Protection": (
#                     'XPATH', "//a[contains(@class,'dropdown-toggle subnav-trigger')][contains(text(),'Protection')]"),
#                 "Investment": (
#                     'XPATH', "//a[contains(@class,'dropdown-toggle subnav-trigger')][contains(text(),'Investment')]"),
#                 "About_us": (
#                     'XPATH', "//a[contains(@class,'dropdown-toggle subnav-trigger')][contains(text(),'About us')]"),
#                 "life_moments_links": ('XPATH', "//li[contains(@class,'dropdown nav-item open')]//li//a"),
#                 "active_breadcrumb": ('XPATH', "//ol[@class='breadcrumb']//li[@class='active']")
#                 }
#
#     def clickSigninbtn(self):
#         print(self.signinBtn.get_property('style'))
#         self.signinBtn.click_button()
#         time.sleep(3)
#
#     def verify_signin_form(self):
#         text = self.customerSigninHeader.get_text()
#         time.sleep(1)
#         filename = sys._getframe(1).f_code.co_name
#         self.driver.save_screenshot(filename + ".png")
#         print(text)
#         try:
#             assert text
#             print("done, now closing form")
#             self.close_signin_formbar.click()
#         except:
#             pytest.fail("customer sign in header not present. Sign in form may not have opened.", pytrace=False)
#
#     def verify_list_of_prods_in_dropdown(self):
#         list_items = self.select_a_product.get_all_list_item()
#         count = 0
#         for item in list_items:
#             self.select_a_product.select_element_by_text(item)
#             time.sleep(3)
#             filename = sys._getframe(1).f_code.co_name
#             self.driver.save_screenshot(filename + str(count) + ".png")
#             count = count + 1
#         print(len(list_items))
#         print(list_items)
#
#     def verify_moved_to_get_a_quote(self):
#         self.select_a_product.select_element_by_index(1)
#         time.sleep(3)
#         self.get_a_quote_btn.click_button()
#         time.sleep(3)
#         self.driver.switch_to.window(self.driver.window_handles[1])
#         time.sleep(2)
#         filename = sys._getframe(1).f_code.co_name
#         self.driver.save_screenshot(filename + ".png")
#         title = self.driver.title
#         print(title)
#         try:
#             assert title
#         except:
#             pytest.fail("Title not found", pytrace=False)
#
#     def hover_to_mega_menu(self):
#         self.life_moments.hover()
#         time.sleep(3)
#
#     def hover_to_Protection(self):
#         self.Protection.hover()
#         time.sleep(3)
#
#     def hover_to_Investment(self):
#         self.Investment.hover()
#         time.sleep(3)
#
#     def hover_to_About_us(self):
#         self.About_us.hover()
#         time.sleep(3)
#
#     def get_megamenu_links(self, locator_key):
#         links = self.driver.find_elements_by_xpath("//li[contains(@class,'dropdown nav-item open')]//li//a")
#         linktexts = [link.text for link in links if link.get_attribute("href")]
#         print(linktexts)
#         for linktext in linktexts:
#             if linktext != "":
#                 ele = self.driver.find_element(By.XPATH, self.locators[locator_key][1])
#                 hover = ActionChains(self.driver).move_to_element(ele)
#                 hover.perform()
#                 # self.locators[locator_key].hover()
#                 time.sleep(2)
#                 self.driver.find_element_by_partial_link_text(linktext).click()
#                 time.sleep(3)
#                 breadcrumbtext = self.active_breadcrumb.get_text()
#                 if breadcrumbtext in linktext:
#                     print("breadcrumb text: ", breadcrumbtext)
#                     print("PASSED as correct breadcrumb present")
#                 else:
#                     print("breadcrumb text: ", breadcrumbtext)
#                     pytest.fail("FAILED as breadcrumb not present or incorrect breadcrumb", pytrace=False)
#
#                 self.driver.back()
#         # for link in links:
#         #     if link.get_attribute("href"):
#         #         print(link.text)


def get_elements_from_xpath():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(baseurl)
    element_list = driver.find_elements_by_xpath("//footer[@id='footer']//li/a")
    element_txt_list = [ele.text for ele in element_list if ele.text != ""]
    text_redundant = ["Follow us on YouTube",
                      "Follow us on Facebook",
                      "Follow us on instagram",
                      "Follow us on Twitter",
                      "Follow us on Linkedin"
                      ]
    result = filter(lambda x: x not in text_redundant, element_txt_list)
    # print(len(list(filtered_ele_texts)))
    return result


@pytest.mark.usefixtures("driver", "homeObj", "fundCalcobj")
class TestExample():
    def test_00_check_for_broken_links(self):
        URL = "https://www.sunlife.co.id/ID/Life+Moments?vgnLocale=en_CA"
        check_for_broken_links(URL)

    def test_01_verify_title(self, driver, homeObj):
        print(driver.title)
        try:
            assert driver.title
        except:
            pytest.fail("page title not present", pytrace=False)

    def test_02_verify_signin_form_present(self, driver, homeObj):
        homeObj.clickSigninbtn()
        homeObj.verify_signin_form()

    def test_03_verify_get_a_quote_list(self, driver, homeObj):
        homeObj.verify_list_of_prods_in_dropdown()

    def test_04_select_a_product_and_get_a_quote(self, driver, homeObj):
        homeObj.verify_moved_to_get_a_quote()

    def test_05_open_mega_menu_life_moments(self, homeObj):
        homeObj.hover_to_mega_menu()

    def test_06_life_moments_megamenu_links(self, homeObj):
        homeObj.hover_to_mega_menu()
        homeObj.get_megamenu_links("life_moments")

    # @pytest.mark.parametrize("loc, name",
    #                          [("//footer[@id='footer']", "footer"), ("//div[@id='global-header']", "header")])
    # @pytest.mark.parametrize("url",
    #                          ["https://www.sunlife.co.id/ID/Life+Moments?vgnLocale=en_CA",
    #                           "https://www.sunlife.co.id/ID/Protection?vgnLocale=en_CA"])
    # def test_07_take_snaps_of_element(self, driver, loc, name, url):
    #     # fox = webdriver.Firefox()
    #     driver.get(url)
    #     time.sleep(5)
    #     image = driver.find_element_by_xpath(loc).screenshot_as_png
    #     # driver.save_screenshot(image)
    #     imageStream = io.BytesIO(image)
    #     path = os.path.splitext(os.path.basename(urlsplit(url).path))
    #     # filename=sys._getframe(0).f_code.co_name
    #     im = Image.open(imageStream)
    #     im.save(path[0] + "_" + name + ".png")
    #     res = Img_Comparison(name + ".png", path[0] + "_" + name + ".png", path[0] + "_" + name)
    #     print(path[0] + "_" + name + " comparison result: ")

    # def test_08_header_diff(self):
    #     res = Img_Comparison("header.png", "header.png", "file")
    #     print(res)

    # def test_09_footer_diff(self):
    #     res = Img_Comparison("test_07_take_snaps_of_element.png", "test_07_take_snaps_of_element_2.png", "file")
    #     print(res)

    def sample_name(self):
        picture_page = "https://www.sunlife.co.id/ID/Life+Moments?vgnLocale=en_CA"

        name = os.path.splitext(os.path.basename(urlsplit(picture_page).path))
        print(name[0])

    def test_11_protection_megamenu_links(self, homeObj):
        homeObj.hover_to_Protection()
        homeObj.get_megamenu_links("Protection")

    def test_12_investment_megamenu_links(self, homeObj):
        homeObj.hover_to_Investment()
        homeObj.get_megamenu_links("Investment")

    def test_13_about_us_megamenu_links(self, homeObj):
        homeObj.hover_to_About_us()
        homeObj.get_megamenu_links("About_us")

    def test_14_find_an_advisor_dropdown_list_of_cities(self, homeObj):
        homeObj.list_of_cities_in_dropdown()

    def test_15_move_to_find_an_advisor_page_after_selecting_city(self, homeObj):
        homeObj.verify_moved_to_find_an_advisor_page()

    #
    # def test_16_Clicking_talk_to_an_advisor_moves_to_find_an_advisor_page(self, homeObj):
    #     homeObj.talk_to_an_advisor_today()

    def test_17_discover_your_needs_dropdown_menu_works(self, homeObj):
        homeObj.discover_your_needs_select_list()

    def test_18_financial_calculator(self, homeObj, fundCalcobj):
        homeObj.click_on_calculate_now()
        fundCalcobj.calculate_child_finance()

    def test_19_contact_advisor(self, homeObj, fundCalcobj):
        homeObj.click_on_calculate_now()
        fundCalcobj.contact_advisor_form()

    def test_20_verify_search_suggestions(self, homeObj):
        homeObj.search_suggestions()

    def test_21_verify_language_and_region_section_opens_on_clicking_lang(self, homeObj):
        homeObj.click_language_to_open()

    @pytest.mark.parametrize("expected_breadcrumb, link_locator",
                             get_data())
    def test_22_verify_clicking_on_header_link_moves_to_corresponding_page_and_breadcrumb_is_displayed(self, homeObj,
                                                                                                       expected_breadcrumb,
                                                                                                       link_locator):
        homeObj.check_links_move_to_page_and_display_exp_breadcrumb(expected_breadcrumb, link_locator)

    def test_practice(self):
        # print(get_data())
        text_redundant = ["Follow us on YouTube",
                          "Follow us on Facebook",
                          "Follow us on instagram",
                          "Follow us on Twitter",
                          "Follow us on Linkedin"
                          ]
        # result = filter(lambda x: x not in text_redundant, get_elements_from_xpath())
        result = get_elements_from_xpath()
        type(result)
        for ele in result:
            print(ele)
            # print(ele.text)

    @pytest.mark.parametrize("ele_text", get_elements_from_xpath())
    def test_verify_footer_links_are_working_properly(self, homeObj, ele_text):
        homeObj.check_footer_links_moves_to_new_url(ele_text)


if __name__ == '__main__':
    pytest.main()

import csv
import pytest

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Tests.Home import Homepage, Child_fund_calculator

baseurl = "https://www.sunlife.com.hk/HK?vgnLocale=en_CA"
testdata_filename = "test_data2.csv"


def get_data():
    # Retrieve values from CSV
    with open(testdata_filename) as f:
        data = [(line['expected_breadcrumb'], line['link_locator']) for line in csv.DictReader(f)]
        # print(data)
    return data


def chrome_opt():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
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


def get_links_from_a_webpage():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(baseurl)
    alllinks = driver.find_elements_by_tag_name("a")
    urls = []
    for link in alllinks:
        if "#" not in str(link.get_attribute("href")) and "javascript" not in str(
                link.get_attribute("href")) and "linkedin" not in str(link.get_attribute("href")):
            if link.text != '':
                urls.append((link.text, link.get_attribute("href")))

    return urls


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
    @pytest.mark.parametrize("link_text, url", get_links_from_a_webpage())
    def test_01_check_for_broken_links(self, link_text, url):
        flag = True
        statusCode = None
        try:
            statusCode = requests.get(url).status_code
            if statusCode == 200:
                print(link_text + ":", url, "PASSED with response code:", statusCode)
            else:
                print(link_text + ":", url, "FAILED with response code:", statusCode)
                flag = False
        except Exception as err:
            print("Something went wrong: ", err)
        if flag == False:
            pytest.fail("Link Maybe Broken...{}".format(statusCode), pytrace=False)

    # def test_02_verify_title(self, driver, homeObj):
    #     print(driver.title)
    #     try:
    #         assert driver.title
    #     except:
    #         pytest.fail("page title not present", pytrace=False)

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

    # def sample_name(self):
    #     picture_page = "https://www.sunlife.co.id/ID/Life+Moments?vgnLocale=en_CA"
    #
    #     name = os.path.splitext(os.path.basename(urlsplit(picture_page).path))
    #     print(name[0])

    def test_11_protection_megamenu_links(self, homeObj):
        homeObj.hover_to_Protection()
        homeObj.get_megamenu_links("Protection")

    def test_12_investment_megamenu_links(self, homeObj):
        homeObj.hover_to_Investment()
        homeObj.get_megamenu_links("Investment")

    def test_13_about_us_megamenu_links(self, homeObj):
        homeObj.hover_to_About_us()
        homeObj.get_megamenu_links("About_us")

    # def test_14_find_an_advisor_dropdown_list_of_cities(self, homeObj):
    #     homeObj.list_of_cities_in_dropdown()

    # def test_15_move_to_find_an_advisor_page_after_selecting_city(self, homeObj):
    #     homeObj.verify_moved_to_find_an_advisor_page()

    #
    # def test_16_Clicking_talk_to_an_advisor_moves_to_find_an_advisor_page(self, homeObj):
    #     homeObj.talk_to_an_advisor_today()

    def test_17_discover_your_needs_dropdown_menu_works(self, homeObj):
        homeObj.discover_your_needs_select_list()

    # def test_18_financial_calculator(self, homeObj, fundCalcobj):
    #     homeObj.click_on_calculate_now()
    #     fundCalcobj.calculate_child_finance()
    #
    # def test_19_contact_advisor(self, homeObj, fundCalcobj):
    #     homeObj.click_on_calculate_now()
    #     fundCalcobj.contact_advisor_form()

    def test_20_verify_search_suggestions(self, homeObj):
        homeObj.search_suggestions()

    def test_21_verify_language_and_region_section_opens_on_clicking_lang(self, homeObj):
        homeObj.click_language_to_open()

    # @pytest.mark.parametrize("expected_breadcrumb, link_locator",
    #                          get_data())
    # def test_22_verify_clicking_on_header_link_moves_to_corresponding_page_and_breadcrumb_is_displayed(self, homeObj,
    #                                                                                                    expected_breadcrumb,
    #                                                                                                    link_locator):
    #     homeObj.check_links_move_to_page_and_display_exp_breadcrumb(expected_breadcrumb, link_locator)

    # def test_practice(self):
    #     # print(get_data())
    #     text_redundant = ["Follow us on YouTube",
    #                       "Follow us on Facebook",
    #                       "Follow us on instagram",
    #                       "Follow us on Twitter",
    #                       "Follow us on Linkedin"
    #                       ]
    #     # result = filter(lambda x: x not in text_redundant, get_elements_from_xpath())
    #     result = get_elements_from_xpath()
    #     type(result)
    #     for ele in result:
    #         print(ele)
    #         # print(ele.text)

    @pytest.mark.parametrize("ele_text", get_elements_from_xpath())
    def test_verify_footer_links_are_working_properly(self, homeObj, ele_text):
        homeObj.check_footer_links_moves_to_new_url(ele_text)


if __name__ == '__main__':
    pytest.main()

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from SLGI.Pages.Home_SLGI import Home

baseurl = "https://www.sunlifeglobalinvestments.com/"


@pytest.fixture(scope='function', autouse=True)
def driver(request):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument(f"--window-size={1920},{3926}")
    # chrome_options.add_argument("--hide-scrollbars")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(8)
    driver.get(baseurl)

    def driver_teardown():
        print("closing browser")
        driver.close()

    request.addfinalizer(driver_teardown)
    yield driver


@pytest.fixture(scope='function', autouse=True)
def home(driver):
    obj = Home(driver)
    yield obj


@pytest.mark.usefixtures("driver", "home")
class Tests():

    def test_01_verify_page_title(self, driver, home):
        print(home.verify_title())
    #
    # def test_02_verify_signin_btn_is_clickable(self, driver, home):
    #     home.click_signin_btn()
    #
    # def test_03_validate_Products_mega_menu(self, driver, home):
    #     home.verify_megamenu_links("Products_mega_menu")
    #     # driver.find_element_by_xpath("").get_attribute()
    #
    # def test_04_validate_Prices_and_Performance_mega_menu(self, driver, home):
    #     home.verify_megamenu_links("Prices_and_Performance_mega_menu")
    #
    # def test_05_validate_Insights_and_Resources_mega_menu(self, driver, home):
    #     home.verify_megamenu_links("Insights_and_Resources_mega_menu")
    #
    # def test_06_validate_About_us_mega_menu(self, driver, home):
    #     home.verify_megamenu_links("About_us_mega_menu")
    #
    # def test_07_search_functionality(self, driver, home):
    #     home.verify_search()
    #
    # def test_08_validate_Footer_section_2(self, driver, home):
    #     home.verify_footer_quicklinks("footer_section_2")
    #
    # def test_09_validate_Footer_section_1(self, driver, home):
    #     home.verify_footer_quicklinks("footer_section_1")


# @pytest.mark.usefixtures("driver", "home")
# class Tests_URL2():
#
#     def test_10_verify_url2_titles(self, driver, home):
#         driver.get("https://www.sunlifeglobalinvestments.com/Slgi/Prices+and+Performance?vgnLocale=en_CA")
#         home.verify_title()
#

if __name__ == '__main__':
    pytest.main()

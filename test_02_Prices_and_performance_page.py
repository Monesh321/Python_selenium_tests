import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

baseurl="https://www.sunlifeglobalinvestments.com/Slgi/Prices+and+Performance?vgnLocale=en_CA"

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



@pytest.mark.usefixtures("driver", "home")
class Tests():

    def test_10_verify_url2_titles(self, driver, home):
        # driver.get("https://www.sunlifeglobalinvestments.com/Slgi/Prices+and+Performance?vgnLocale=en_CA")
        home.verify_title()

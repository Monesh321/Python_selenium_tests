import sys
import time
# from pytest_expect import expect
from delayed_assert import expect, assert_expectations

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from seleniumpagefactory import PageFactory


class Common_methods():
    def __init__(self, driver):
        # super().__init__()
        self.driver = driver

    def move_to_page_check_title_breadcrumb_and_return(self, breadcrumb_locator, expected_breadcrumb, link_locator):
        time.sleep(3)
        self.driver.find_element_by_xpath(
            "//div[@id='global-header']//a[contains(text(),'" + link_locator + "')]").click()
        time.sleep(4)
        actual_breadcrumb = self.driver.find_element_by_xpath(breadcrumb_locator).text

        try:
            print("ACTUAL:", actual_breadcrumb)
            print("EXPECTED:", expected_breadcrumb)
            print("TITLE:", self.driver.title)
            assert expected_breadcrumb in actual_breadcrumb
            print("PASSED: breadcrumb {} present in page".format(actual_breadcrumb))
        except:
            pytest.fail("FAILED: No Breadcrumb Present")

    def check_footer_links_moves_to_new_url(self, ele_text):
        try:
            time.sleep(1)
            self.driver.find_element_by_partial_link_text(ele_text).click()
            print("TITLE:", self.driver.title)
        except Exception as err:
            print("webelement : ", ele_text, "ERROR: ", err)
            pytest.fail("link not working or moved to incorrect page", pytrace=False)


@pytest.mark.usefixtures("driver")
class Homepage(PageFactory, Common_methods):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    locators = {"signinBtn": ('XPATH', "//a[@id='signinbutton']"),
                "customerSigninHeader": ('XPATH', "//div[@id='customerSignInHeader']"),
                "close_signin_formbar": ('XPATH', "//button[@class='close-modal']"),
                "select_a_product": ('XPATH', "//select[@id='select-product']"),
                "get_a_quote_btn": ('XPATH', "//input[@id='get-a-quote-btn']"),
                "life_moments": (
                    'XPATH', "//a[contains(@class,'dropdown-toggle subnav-trigger')][contains(text(),'Life Moments')]"),
                "Protection": (
                    'XPATH', "//a[contains(@class,'dropdown-toggle subnav-trigger')][contains(text(),'Protection')]"),
                "Investment": (
                    'XPATH', "//a[contains(@class,'dropdown-toggle subnav-trigger')][contains(text(),'Investment')]"),
                "About_us": (
                    'XPATH', "//a[contains(@class,'dropdown-toggle subnav-trigger')][contains(text(),'About us')]"),
                "life_moments_links": ('XPATH', "//li[contains(@class,'dropdown nav-item open')]//li//a"),
                "active_breadcrumb": ('XPATH', "//ol[@class='breadcrumb']//li[@class='active']"),
                "find_an_advisor": ('XPATH', "//select[@id='id_sign_in_faa']"),
                "submit_btn": ('XPATH', "//div[@id='submit_faa']//*[contains(text(),'Submit')]"),
                "talk_to_an_advisor": ('XPATH', "//a[contains(text(),'Talk to an advisor today')]"),
                "discover_needs": ('XPATH', "//select[@id='bc_q1_1_ans_select_1']"),
                "my_purpose1": ('XPATH', "//select[@id='bc_q2_1_ans_select_1']"),
                "my_purpose2": ('XPATH', "//select[@id='bc_q2_1_ans_select_2']"),
                "submit2": ('XPATH', "//a[@class='btn btn-blue at-element-click-tracking'][contains(text(),'Submit')]"),
                "calculate_now": ('XPATH', "//a[contains(text(),'Calculate now')]"),
                "search_link": ('XPATH', "//a[contains(text(),'Search')]"),
                "search_input_box": ('XPATH', "//input[@id='q-top']"),
                "search_autocomplete": ('XPATH', "//div[@class='search-autocomplete']/ul"),
                "language_and_region_links": ('XPATH', "//div[@id='language-top']//li/a"),
                "language_btn": ('XPATH', "//div[@id='language-btn']"),
                "close_language_section": (
                    'XPATH', "//div[@class='col-md-12 text-right']//span[@class='fa fa-remove collapse-x']"),
                "footer_xpath": ('XPATH', "//footer[@id='footer']//li/a")
                }

    def get_elements_from_xpath(self):
        element_list = self.driver.find_elements_by_xpath(self.locators["footer_xpath"][1])
        return element_list

    def check_links_move_to_page_and_display_exp_breadcrumb(self, expected_breadcrumb, link_locator):
        self.move_to_page_check_title_breadcrumb_and_return(self.locators["active_breadcrumb"][1], expected_breadcrumb,
                                                            link_locator)

    def clickSigninbtn(self):
        print(self.signinBtn.get_property('style'))
        self.signinBtn.click_button()
        time.sleep(3)

    def verify_signin_form(self):
        text = self.customerSigninHeader.get_text()
        time.sleep(1)
        filename = sys._getframe(1).f_code.co_name
        self.driver.save_screenshot(filename + ".png")
        print(text)
        try:
            assert text
            print("done, now closing form")
            self.close_signin_formbar.click()
        except:
            pytest.fail("customer sign in header not present. Sign in form may not have opened.", pytrace=False)

    def verify_list_of_prods_in_dropdown(self):
        list_items = self.select_a_product.get_all_list_item()
        count = 0
        for item in list_items:
            self.select_a_product.select_element_by_text(item)
            time.sleep(3)
            filename = sys._getframe(1).f_code.co_name
            self.driver.save_screenshot(filename + str(count) + ".png")
            count = count + 1
        print(len(list_items))
        print(list_items)
        try:
            assert len(list_items) == 3
        except:
            pytest.fail("some items in dropdown list maybe missing :FAILED", pytrace=False)

    def verify_moved_to_get_a_quote(self):
        self.select_a_product.select_element_by_index(1)
        time.sleep(3)
        self.get_a_quote_btn.click_button()
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(2)
        filename = sys._getframe(1).f_code.co_name
        self.driver.save_screenshot(filename + ".png")
        title = self.driver.title
        print(title)
        try:
            assert title
        except:
            pytest.fail("Title not found", pytrace=False)

    def hover_to_mega_menu(self):
        self.life_moments.hover()
        time.sleep(3)

    def hover_to_Protection(self):
        self.Protection.hover()
        time.sleep(3)

    def hover_to_Investment(self):
        self.Investment.hover()
        time.sleep(3)

    def hover_to_About_us(self):
        self.About_us.hover()
        time.sleep(3)

    def get_megamenu_links(self, locator_key):
        links = self.driver.find_elements_by_xpath("//li[contains(@class,'dropdown nav-item open')]//li//a")
        linktexts = [link.text for link in links if link.get_attribute("href")]
        print(linktexts)
        for linktext in linktexts:
            if linktext != "":
                ele = self.driver.find_element(By.XPATH, self.locators[locator_key][1])
                hover = ActionChains(self.driver).move_to_element(ele)
                hover.perform()
                # self.locators[locator_key].hover()
                time.sleep(2)
                self.driver.find_element_by_partial_link_text(linktext).click()
                time.sleep(3)
                breadcrumbtext = self.active_breadcrumb.get_text()
                if breadcrumbtext in linktext:
                    print("breadcrumb text: ", breadcrumbtext)
                    print("PASSED as correct breadcrumb present")
                else:
                    print("breadcrumb text: ", breadcrumbtext)
                    pytest.fail("FAILED as breadcrumb not present or incorrect breadcrumb", pytrace=False)

                self.driver.back()

    def list_of_cities_in_dropdown(self):
        list_items = self.find_an_advisor.get_all_list_item()
        count = 0
        for item in list_items:
            self.find_an_advisor.select_element_by_text(item)
            time.sleep(3)
            filename = sys._getframe(1).f_code.co_name
            self.driver.save_screenshot(filename + str(count) + ".png")
            count = count + 1
        print(len(list_items))
        print(list_items)
        try:
            assert len(list_items) == 16
        except:
            pytest.fail("some items in dropdown list maybe missing :FAILED", pytrace=False)

    def verify_moved_to_find_an_advisor_page(self):
        currenturl = self.driver.current_url
        self.find_an_advisor.select_element_by_index(1)
        time.sleep(4)
        self.submit_btn.click_button()
        time.sleep(3)
        newurl = self.driver.current_url
        filename = sys._getframe(1).f_code.co_name
        self.driver.save_screenshot(filename + ".png")
        title = self.driver.title
        print(title)
        try:
            assert currenturl != newurl
            assert title
        except:
            pytest.fail("Title not found or wrong url", pytrace=False)

    def talk_to_an_advisor_today(self):
        currenturl = self.driver.current_url
        time.sleep(2)
        self.driver.find_element_by_xpath(self.locators["talk_to_an_advisor"][1]).click()
        time.sleep(3)
        newurl = self.driver.current_url
        title = self.driver.title
        print(title)
        try:
            assert currenturl != newurl
            assert title
        except:
            pytest.fail("Title not found or wrong url", pytrace=False)

    def discover_your_needs_select_list(self):
        list = self.discover_needs.get_all_list_item()
        print(list)
        for item in list:
            if item != "":
                self.discover_needs.select_element_by_text(item)
                time.sleep(2)
                if item == "Get protected":
                    self.my_purpose1.select_element_by_index(1)
                    self.driver.find_element_by_xpath(self.locators["submit2"][1]).click()
                elif item == "Plan my future":
                    self.my_purpose2.select_element_by_index(1)
                    self.driver.find_element_by_xpath(self.locators["submit2"][1]).click()
                time.sleep(4)
                title = self.driver.title
                print(title)
                self.driver.back()
                if "Planner and Advice" not in title:
                    pytest.fail("Expected page title did not match.May not have moved to correct page", pytrace=False)
                else:
                    print("PASSED")

    def click_on_calculate_now(self):
        self.calculate_now.click_button()
        time.sleep(2)

    def search_suggestions(self):
        self.search_link.click_button()
        time.sleep(1)
        self.search_input_box.set_text("insurance")
        time.sleep(3)
        suggestions = self.driver.find_elements_by_xpath(self.locators["search_autocomplete"][1])
        for element in suggestions:
            print(element.text)

    def click_language_to_open(self):
        self.language_btn.click_button()
        links = self.driver.find_elements_by_xpath(self.locators["language_and_region_links"][1])
        for link in links:
            print(link.text)

        self.close_language_section.click_button()
        print("completed")


class Child_fund_calculator(PageFactory):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    locators = {"playgroup": ('XPATH', "//input[@id='playgroup']"),
                "kindergarten": ('XPATH', "//input[@id='tk']"),
                "elementary_school": ('XPATH', "//input[@id='sd']"),
                "junior_high": ('XPATH', "//input[@id='smp']"),
                "senior_high": ('XPATH', "//input[@id='sma']"),
                "bachelors": ('XPATH', "//input[@id='s1']"),
                "masters": ('XPATH', "//input[@id='s2']"),
                "childs_birth": ('XPATH', "//select[@id='lahir']"),
                "calculate": ('XPATH', "//input[@id='submit']"),
                "table_title": ('XPATH', "//div[@class='title-main text-center']"),
                "active_breadcrumb": ('XPATH', "//ol[@class='breadcrumb']//li[@class='active']"),
                "contact_advisor": ('XPATH', "//input[@id='slf-leadgen-first-name']"),
                "radio_btn_client": ('XPATH', "//label[@class='btn btn-blue-lead']"),
                "radio_btn_non_client": ('XPATH', "//input[@type='radio'][@id='option1']"),
                "mobile": ('XPATH', "//input[@id='slf-leadgen-phone-number']"),
                "email": ('XPATH', "//input[@id='slf-leadgen-email-address']"),
                "city": ('XPATH', "//select[@id='city_name']"),
                "submit_btn": ('XPATH', "//button[@id='advisor-modal-submit-btn']"),
                "thank_you": ('XPATH', "//p[contains(text(),'Thank you for submitting your contact details. Our')]"),
                "ok_btn": ('XPATH', "//button[@class='btn btn-yellow text-center']")
                }

    def calculate_child_finance(self):

        title = self.driver.title
        print(title)
        breadcrumb = self.active_breadcrumb.visibility_of_element_located(timeout=6)
        try:
            assert title
            assert breadcrumb
        except:
            pytest.fail("titlenot found", pytrace=False)
        time.sleep(5)
        self.playgroup.set_text(1000)
        self.kindergarten.set_text(1000)
        self.elementary_school.set_text(1000)
        self.junior_high.set_text(800)
        self.senior_high.set_text(500)
        self.bachelors.set_text(1200)
        self.masters.set_text(75)
        time.sleep(1)
        allyears = self.childs_birth.get_all_list_item()
        time.sleep(1)
        print(allyears)
        self.childs_birth.select_element_by_index(11)
        time.sleep(2)
        self.calculate.click_button()
        try:
            assert self.table_title.get_text()
            print(self.table_title.get_text(), ": PASSED")
        except:
            pytest.fail("calculation table title not present.Unable to calculate", pytrace=False)

    def contact_advisor_form(self):
        self.contact_advisor.set_text("Monesh Ali")
        self.radio_btn_client.click_button()
        self.mobile.set_text("62812124567")
        self.email.set_text("monesh321@gmail.com")
        list = self.city.get_all_list_item()
        print(list)
        self.city.select_element_by_index(4)
        self.submit_btn.click_button()
        no_of_windows = self.driver.window_handles
        print(no_of_windows)
        print("pop up opened")
        time.sleep(1)
        # self.driver.switch_to.active_element()
        window_message = self.thank_you.get_text()
        print(window_message)
        # time.sleep(2)
        expect(
            window_message == "Thank you for submitting your contact details. Our advisor will be in touch with you soon.")
        self.ok_btn.click_button()
        print("Completed")
        assert_expectations()

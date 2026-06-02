from pages.base_page import BasePage
from locators.practice_test_exception_locators import PracticeTestExceptionLocators
from playwright.sync_api import expect
import allure

class PracticeTestAutomationExceptionPage(BasePage):
    
    def open_browser(self, url):
        self.page.goto(url)
        self.click(PracticeTestExceptionLocators.EXCEPTION_PAGE)
        expect(self.page).to_have_url("https://practicetestautomation.com/practice-test-exceptions/")
        self.is_visible(PracticeTestExceptionLocators.EXCEPTION_PAGE_HEADER)
        expect(self.page.locator(PracticeTestExceptionLocators.EXCEPTION_PAGE_HEADER)).to_contain_text("Test Exceptions")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Exception_Page_Header", attachment_type=allure.attachment_type.PNG)

    def edit_row(self):
        self.is_visible(PracticeTestExceptionLocators.ROW_ONE_TEXT)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_ONE_TEXT)).to_contain_text("Row 1")
        self.is_visible(PracticeTestExceptionLocators.ROW_ONE_EDIT_BUTTON)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_ONE_EDIT_BUTTON)).to_be_enabled()
        self.click(PracticeTestExceptionLocators.ROW_ONE_EDIT_BUTTON)
        self.is_visible(PracticeTestExceptionLocators.ROW_ONE_INPUT_FIELD)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_ONE_INPUT_FIELD)).to_be_enabled()
        self.clear_text(PracticeTestExceptionLocators.ROW_ONE_INPUT_FIELD)
        self.fill(PracticeTestExceptionLocators.ROW_ONE_INPUT_FIELD, "Burger")
        self.is_visible(PracticeTestExceptionLocators.ROW_ONE_SAVE_BUTTON)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_ONE_SAVE_BUTTON)).to_be_enabled()
        self.click(PracticeTestExceptionLocators.ROW_ONE_SAVE_BUTTON)
        self.is_visible(PracticeTestExceptionLocators.ROW_ONE_SAVE_SUCCESS_MSG)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_ONE_SAVE_SUCCESS_MSG)).to_contain_text("Row 1 was saved")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Row_One_Save_Success_Message", attachment_type=allure.attachment_type.PNG)

    def add_row(self):
        self.is_visible(PracticeTestExceptionLocators.ROW_ONE_TEXT)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_ONE_TEXT)).to_contain_text("Row 1")
        self.is_visible(PracticeTestExceptionLocators.ROW_ONE_ADD_BUTTON)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_ONE_ADD_BUTTON)).to_be_enabled()
        self.click(PracticeTestExceptionLocators.ROW_ONE_ADD_BUTTON)
        self.is_visible(PracticeTestExceptionLocators.ROW_TWO_ADD_MSG)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_TWO_ADD_MSG)).to_contain_text("Row 2 was added")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Row_Two_Added_Success_Message", attachment_type=allure.attachment_type.PNG)
        self.is_visible(PracticeTestExceptionLocators.ROW_TWO_INPUT_FIELD)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_TWO_INPUT_FIELD)).to_be_enabled()
        self.clear_text(PracticeTestExceptionLocators.ROW_TWO_INPUT_FIELD)
        self.fill(PracticeTestExceptionLocators.ROW_TWO_INPUT_FIELD, "Pizza")
        self.is_visible(PracticeTestExceptionLocators.ROW_TWO_SAVE_BUTTON)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_TWO_SAVE_BUTTON)).to_be_enabled()
        self.click(PracticeTestExceptionLocators.ROW_TWO_SAVE_BUTTON)
        self.is_visible(PracticeTestExceptionLocators.ROW_TWO_SAVE_SUCCESS_MSG)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_TWO_SAVE_SUCCESS_MSG)).to_contain_text("Row 2 was saved")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Row_Two_Save_Success_Message", attachment_type=allure.attachment_type.PNG)

    def remove_row(self):
        self.is_visible(PracticeTestExceptionLocators.ROW_ONE_TEXT)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_ONE_TEXT)).to_contain_text("Row 1")
        self.is_visible(PracticeTestExceptionLocators.ROW_ONE_ADD_BUTTON)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_ONE_ADD_BUTTON)).to_be_enabled()
        self.click(PracticeTestExceptionLocators.ROW_ONE_ADD_BUTTON)
        self.is_visible(PracticeTestExceptionLocators.ROW_TWO_ADD_MSG)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_TWO_ADD_MSG)).to_contain_text("Row 2 was added")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Row_Two_Added_Success_Message", attachment_type=allure.attachment_type.PNG)
        self.is_visible(PracticeTestExceptionLocators.ROW_TWO_REMOVE_BUTTON)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_TWO_REMOVE_BUTTON)).to_be_enabled()
        self.click(PracticeTestExceptionLocators.ROW_TWO_REMOVE_BUTTON)
        self.page.wait_for_timeout(2000)
        self.is_visible(PracticeTestExceptionLocators.ROW_TWO_REMOVE_MSG)
        expect(self.page.locator(PracticeTestExceptionLocators.ROW_TWO_REMOVE_MSG)).to_contain_text("Row 2 was removed")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Row_Two_Remove_Success_Message", attachment_type=allure.attachment_type.PNG)





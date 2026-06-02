from pages.base_page import BasePage
from locators.practice_test_login_locators import PracticeTestLoginLocators
from playwright.sync_api import expect
import allure

class PracticeTestAutomationLoginPage(BasePage):
    
    def open_browser(self, url):
        self.page.goto(url)
        self.click(PracticeTestLoginLocators.LOGIN_PAGE)
        expect(self.page).to_have_url("https://practicetestautomation.com/practice-test-login/")

    def login_with_valid_credentials(self):
        self.click(PracticeTestLoginLocators.USER_NAME_INPUT)
        self.fill(PracticeTestLoginLocators.USER_NAME_INPUT, "student")
        self.click(PracticeTestLoginLocators.LOGIN_PASSWORD_INPUT)
        self.fill(PracticeTestLoginLocators.LOGIN_PASSWORD_INPUT, "Password123")
        self.is_visible(PracticeTestLoginLocators.SIGNIN_SUBMIT_BUTTON)
        self.click(PracticeTestLoginLocators.SIGNIN_SUBMIT_BUTTON)
        self.is_visible(PracticeTestLoginLocators.LOGIN_SUCCESS_MSG)
        expect(self.page.locator(PracticeTestLoginLocators.LOGIN_SUCCESS_MSG)).to_contain_text("Logged In Successfully")
        self.is_visible(PracticeTestLoginLocators.LOGIN_SUCCESS_MSG_ONE)
        expect(self.page.locator(PracticeTestLoginLocators.LOGIN_SUCCESS_MSG_ONE)).to_contain_text("Congratulations student. You successfully logged in!")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Login_Success_Message", attachment_type=allure.attachment_type.PNG)
        self.is_visible(PracticeTestLoginLocators.LOGOUT_BUTTON)
        self.click(PracticeTestLoginLocators.LOGOUT_BUTTON)

    def login_with_invalid_id(self):
        self.click(PracticeTestLoginLocators.USER_NAME_INPUT)
        self.fill(PracticeTestLoginLocators.USER_NAME_INPUT, "incorrectUser")
        self.click(PracticeTestLoginLocators.LOGIN_PASSWORD_INPUT)
        self.fill(PracticeTestLoginLocators.LOGIN_PASSWORD_INPUT, "Password123")
        self.is_visible(PracticeTestLoginLocators.SIGNIN_SUBMIT_BUTTON)
        self.click(PracticeTestLoginLocators.SIGNIN_SUBMIT_BUTTON)
        self.is_visible(PracticeTestLoginLocators.INVALID_USERNAME_MSG)
        expect(self.page.locator(PracticeTestLoginLocators.INVALID_USERNAME_MSG)).to_contain_text("Your username is invalid!")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Invalid_Username_Message", attachment_type=allure.attachment_type.PNG)

    def login_with_invalid_password(self):
        self.click(PracticeTestLoginLocators.USER_NAME_INPUT)
        self.fill(PracticeTestLoginLocators.USER_NAME_INPUT, "student")
        self.click(PracticeTestLoginLocators.LOGIN_PASSWORD_INPUT)
        self.fill(PracticeTestLoginLocators.LOGIN_PASSWORD_INPUT, "incorrectPassword")
        self.is_visible(PracticeTestLoginLocators.SIGNIN_SUBMIT_BUTTON)
        self.click(PracticeTestLoginLocators.SIGNIN_SUBMIT_BUTTON)
        self.is_visible(PracticeTestLoginLocators.INVALID_PASSWORD_MSG)
        expect(self.page.locator(PracticeTestLoginLocators.INVALID_PASSWORD_MSG)).to_contain_text("Your password is invalid!")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Invalid_Password_Message", attachment_type=allure.attachment_type.PNG)



from pages.base_page import BasePage
from locators.aw_locators import AwLocators
from utils.healing_engine import generate_locators
from playwright.sync_api import expect
import allure

class LoginPage(BasePage):

    def open_browser(self, url):
        self.page.goto(url)

    #def login(self, username, password):
    def login(self):
        #self.fill(AwLocators.USERNAME_INPUT, username)
        self.fill(AwLocators.USERNAME_INPUT, "LB-WizardAdmin")
        #self.fill(AwLocators.PASSWORD_INPUT, password)
        self.fill(AwLocators.PASSWORD_INPUT, "~h34`G4u=")
        self.click(AwLocators.SIGN_IN_BUTTON)
        self.is_visible(AwLocators.AW_LAUNCH_BTN)
        self.click(AwLocators.AW_LAUNCH_BTN)

    #def login_with_invalid_credentials(self, username, password):
    def login_with_invalid_credentials(self):
        self.fill(AwLocators.USERNAME_INPUT, "LB-WizardAdmin")
        self.fill(AwLocators.PASSWORD_INPUT, "xyz")
        self.click(AwLocators.SIGN_IN_BUTTON)
        self.is_visible(AwLocators.AW_INVALID_CREDENTIALS_MSG)
        expect(self.page.locator(AwLocators.AW_INVALID_CREDENTIALS_MSG)).to_contain_text("We didn't recognize the username or password you entered. Please try again.")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Invalid_Credentials_Login_Attempt", attachment_type=allure.attachment_type.PNG)



    


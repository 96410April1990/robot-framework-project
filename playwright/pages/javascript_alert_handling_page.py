from pages.base_page import BasePage
from locators.javascript_alert_handling_locators import JavascriptAlertHandlingLocators
from playwright.sync_api import expect
import allure

class JavascriptAlertHandlingPage(BasePage):
    
    def open_browser(self):
        self.page.goto("https://the-internet.herokuapp.com/javascript_alerts?utm_source=chatgpt.com")
        self.is_visible(JavascriptAlertHandlingLocators.ALERT_HOMEPAGE_HEADER)
        expect(self.page.locator(JavascriptAlertHandlingLocators.ALERT_HOMEPAGE_HEADER)).to_contain_text("JavaScript Alerts")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="JavaScript_Alerts_Home_Page", attachment_type=allure.attachment_type.PNG)

    def handle_js_alert(self):
        self.is_visible(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_BUTTON)
        expect(self.page.locator(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_BUTTON)).to_be_enabled()
        self.click(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_BUTTON)
        self.accept_alert()

    def handle_js_confirm(self, accept: bool):
        self.is_visible(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_CONFIRM)
        expect(self.page.locator(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_CONFIRM)).to_be_enabled()
        if accept:
            self.accept_alert()
        else:
            self.dismiss_alert()
        self.click(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_CONFIRM)
        if accept:
            self.is_visible(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_CONFIRM_RESULT)
            expect(self.page.locator(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_CONFIRM_RESULT)).to_contain_text("You clicked: Ok")
            screenshot = self.page.screenshot()
            allure.attach(screenshot, name="JS_Confirm_Accepted", attachment_type=allure.attachment_type.PNG)
        else:
            self.is_visible(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_CONFIRM_RESULT)
            expect(self.page.locator(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_CONFIRM_RESULT)).to_contain_text("You clicked: Cancel")
            screenshot = self.page.screenshot()
            allure.attach(screenshot, name="JS_Confirm_Dismissed", attachment_type=allure.attachment_type.PNG)

    def handle_js_prompt(self, accept: bool):
        self.is_visible(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_PROMPT)
        expect(self.page.locator(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_PROMPT)).to_be_enabled()
        if accept:
            self.accept_prompt("Playwright test validation")
        else:
            self.dismiss_prompt("Playwright test validation")
        self.click(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_PROMPT)
        if accept:
            self.is_visible(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_PROMPT_RESULT)
            expect(self.page.locator(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_PROMPT_RESULT)).to_contain_text("You entered: Playwright test validation")
            screenshot = self.page.screenshot()
            allure.attach(screenshot, name="JS_Prompt_Accepted", attachment_type=allure.attachment_type.PNG)
        else:
            self.is_visible(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_PROMPT_RESULT)
            expect(self.page.locator(JavascriptAlertHandlingLocators.ALERT_JS_ALERT_PROMPT_RESULT)).to_contain_text("You entered: null")
            screenshot = self.page.screenshot()
            allure.attach(screenshot, name="JS_Prompt_Dismissed", attachment_type=allure.attachment_type.PNG)
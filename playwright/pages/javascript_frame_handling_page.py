from pages.base_page import BasePage
from locators.javascript_frame_handling_locators import JavascriptFrameHandlingLocators
from playwright.sync_api import expect
import allure

class JavascriptFrameHandlingPage(BasePage):
    
    def open_browser(self):
        self.page.goto("https://the-internet.herokuapp.com/iframe?utm_source=chatgpt.com")
        self.is_visible(JavascriptFrameHandlingLocators.FRAME_HOMEPAGE_HEADER)
        expect(self.page.locator(JavascriptFrameHandlingLocators.FRAME_HOMEPAGE_HEADER)).to_contain_text("An iFrame containing the TinyMCE WYSIWYG Editor")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Handle_Frame_Home_Page", attachment_type=allure.attachment_type.PNG)
    
    def handle_frame(self):
        self.is_visible(JavascriptFrameHandlingLocators.FRAME_IFRAME)
        expect(self.page.locator(JavascriptFrameHandlingLocators.FRAME_IFRAME)).to_be_enabled()
        frame = self.page.frame_locator(JavascriptFrameHandlingLocators.FRAME_IFRAME)
        frame.locator(JavascriptFrameHandlingLocators.FRAME_CONTENT_TEXT).wait_for(state="visible")
        expect(frame.locator(JavascriptFrameHandlingLocators.FRAME_CONTENT_TEXT)).to_contain_text("Your content goes here.")
        
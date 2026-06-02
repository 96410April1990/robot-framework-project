from pages.base_page import BasePage
from locators.javascript_window_handling_locators import JavascriptWindowHandlingLocators
from playwright.sync_api import expect
import allure

class JavascriptWindowHandlingPage(BasePage):
    
    def open_browser(self):
        self.page.goto("https://the-internet.herokuapp.com/windows?utm_source=chatgpt.com")
        self.is_visible(JavascriptWindowHandlingLocators.WINDOW_HOMEPAGE_HEADER)
        expect(self.page.locator(JavascriptWindowHandlingLocators.WINDOW_HOMEPAGE_HEADER)).to_contain_text("Opening a new window")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Handle_Window_Home_Page", attachment_type=allure.attachment_type.PNG)
    
    def handle_new_window(self):
        self.is_visible(JavascriptWindowHandlingLocators.WINDOW_CLICK_HERE_LINK)
        expect(self.page.locator(JavascriptWindowHandlingLocators.WINDOW_CLICK_HERE_LINK)).to_be_enabled()
        with self.page.expect_popup() as popup_info:
            self.click(JavascriptWindowHandlingLocators.WINDOW_CLICK_HERE_LINK)
        new_page = popup_info.value
        new_page.wait_for_load_state()
        expect(new_page).to_have_url("https://the-internet.herokuapp.com/windows/new")
        new_page.is_visible(JavascriptWindowHandlingLocators.WINDOW_NEW_PAGE_HEADER)
        expect(new_page.locator(JavascriptWindowHandlingLocators.WINDOW_NEW_PAGE_HEADER)).to_be_enabled()
        expect(new_page.locator(JavascriptWindowHandlingLocators.WINDOW_NEW_PAGE_HEADER)).to_contain_text("New Window")
        screenshot = new_page.screenshot()
        allure.attach(screenshot, name="New_Window_Page_Header", attachment_type=allure.attachment_type.PNG)
        new_page.close()
        print('Back to the original page', self.page.title())

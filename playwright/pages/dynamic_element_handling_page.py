from pages.base_page import BasePage
from locators.dynamic_element_handling_locators import DynamicElementHandlingLocators
from playwright.sync_api import expect
import allure

class DynamicElementHandlingPage(BasePage):
    
    def open_browser(self):
        self.page.goto("https://the-internet.herokuapp.com/dynamic_loading?utm_source=chatgpt.com")
        self.is_visible(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_HOMEPAGE_HEADER)
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_HOMEPAGE_HEADER)).to_contain_text("Dynamically Loaded Page Elements")
        self.is_visible(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_HOME_PAGE_TEXT_ONE)
        self.is_visible(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_HOME_PAGE_TEXT_TWO)
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Dynamic_Element_Home_Page", attachment_type=allure.attachment_type.PNG)

    def handle_hidden_element(self):
        self.is_visible(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_ONE)
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_ONE)).to_be_enabled()
        self.click(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_ONE)
        self.is_visible(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_ONE_TEXT)
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_ONE_TEXT)).to_be_enabled()
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_ONE_TEXT)).to_contain_text("Example 1: Element on page that is hidden")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Dynamic_Element_1_Home_Page_Before_Click", attachment_type=allure.attachment_type.PNG)
        self.is_visible(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_ONE_START_BUTTON)
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_ONE_START_BUTTON)).to_be_enabled()
        self.click(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_ONE_START_BUTTON)
        self.is_visible(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_ONE_ENABLED)
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_ONE_ENABLED)).to_be_enabled()
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_ONE_ENABLED)).to_contain_text("Hello World!")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Dynamic_Element_1_Home_Page_After_Click", attachment_type=allure.attachment_type.PNG)

    def handle_rendered_element(self):
        self.is_visible(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_TWO)
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_TWO)).to_be_enabled()
        self.click(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_TWO)
        self.is_visible(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_TWO_TEXT)
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_TWO_TEXT)).to_be_enabled()
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_TWO_TEXT)).to_contain_text("Example 2: Element rendered after the fact")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Dynamic_Element_2_Home_Page_Before_Click", attachment_type=allure.attachment_type.PNG)
        self.is_visible(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_TWO_START_BUTTON)
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_TWO_START_BUTTON)).to_be_enabled()
        self.click(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_TWO_START_BUTTON)
        self.is_visible(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_TWO_ENABLED)
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_TWO_ENABLED)).to_be_enabled()
        expect(self.page.locator(DynamicElementHandlingLocators.DYNAMIC_ELEMENT_TWO_ENABLED)).to_contain_text("Hello World!")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Dynamic_Element_2_Home_Page_After_Click", attachment_type=allure.attachment_type.PNG)
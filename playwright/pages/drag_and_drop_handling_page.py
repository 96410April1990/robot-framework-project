from pages.base_page import BasePage
from locators.drag_and_drop_handling_locators import DragAndDropHandlingLocators
from playwright.sync_api import expect
import allure

class DragAndDropHandlingPage(BasePage):
    
    def open_browser(self):
        self.page.goto("https://the-internet.herokuapp.com/drag_and_drop?utm_source=chatgpt.com")
        self.is_visible(DragAndDropHandlingLocators.DRAG_AND_DROP_HOMEPAGE_HEADER)
        expect(self.page.locator(DragAndDropHandlingLocators.DRAG_AND_DROP_HOMEPAGE_HEADER)).to_contain_text("Drag and Drop")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Drag_and_Drop_Home_Page", attachment_type=allure.attachment_type.PNG)

    def drag_and_drop_item(self):
        self.is_visible(DragAndDropHandlingLocators.DRAG_AND_DROP_ITEM_A)
        expect(self.page.locator(DragAndDropHandlingLocators.DRAG_AND_DROP_ITEM_A)).to_be_enabled()
        self.is_visible(DragAndDropHandlingLocators.DRAG_AND_DROP_ITEM_B)
        expect(self.page.locator(DragAndDropHandlingLocators.DRAG_AND_DROP_ITEM_B)).to_be_enabled()
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="Before_Drag_And_Drop", attachment_type=allure.attachment_type.PNG)
        self.drag_and_drop(DragAndDropHandlingLocators.DRAG_AND_DROP_ITEM_A, DragAndDropHandlingLocators.DRAG_AND_DROP_ITEM_B)
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="After_Drag_And_Drop", attachment_type=allure.attachment_type.PNG)
        
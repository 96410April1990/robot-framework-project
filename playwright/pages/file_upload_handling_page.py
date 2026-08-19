from pages.base_page import BasePage
from locators.file_upload_handling_locators import FileUploadHandlingLocators
from playwright.sync_api import expect
import allure

class FileUploadHandlingPage(BasePage):
    
    def open_browser(self):
        self.page.goto("https://the-internet.herokuapp.com/upload?utm_source=chatgpt.com")
        self.is_visible(FileUploadHandlingLocators.FILE_UPLOAD_HOMEPAGE_HEADER)
        expect(self.page.locator(FileUploadHandlingLocators.FILE_UPLOAD_HOMEPAGE_HEADER)).to_contain_text("File Uploader")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="File_Uploader_Home_Page", attachment_type=allure.attachment_type.PNG)

    def upload_file(self):
        self.is_visible(FileUploadHandlingLocators.FILE_UPLOAD_CHOOSE_FILE_BTN)
        expect(self.page.locator(FileUploadHandlingLocators.FILE_UPLOAD_CHOOSE_FILE_BTN)).to_be_enabled()
        self.file_upload(FileUploadHandlingLocators.FILE_UPLOAD_CHOOSE_FILE_BTN, "/Users/rohithnandakumar/Documents/sample_doc.pdf")
        self.is_visible(FileUploadHandlingLocators.FILE_UPLOAD_BTN)
        expect(self.page.locator(FileUploadHandlingLocators.FILE_UPLOAD_BTN)).to_be_enabled()
        self.click(FileUploadHandlingLocators.FILE_UPLOAD_BTN)
        self.is_visible(FileUploadHandlingLocators.FILE_UPLOAD_SUCCESS_MSG)
        expect(self.page.locator(FileUploadHandlingLocators.FILE_UPLOAD_SUCCESS_MSG)).to_contain_text("File Uploaded!")
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name="File_Upload_Success_Message", attachment_type=allure.attachment_type.PNG)
        
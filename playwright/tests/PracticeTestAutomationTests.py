import pytest
import allure
from pages.practice_test_automation_login_page import PracticeTestAutomationLoginPage
from pages.practice_test_automation_exception_page import PracticeTestAutomationExceptionPage
from pages.practice_test_automation_test_table_page import PracticeTestAutomationTestTablePage
from pages.javascript_alert_handling_page import JavascriptAlertHandlingPage
from pages.javascript_windows_handling_page import JavascriptWindowHandlingPage
from pages.javascript_frame_handling_page import JavascriptFrameHandlingPage
from pages.file_upload_handling_page import FileUploadHandlingPage
from pages.drag_and_drop_handling_page import DragAndDropHandlingPage
from pages.dynamic_element_handling_page import DynamicElementHandlingPage
from api.reqres_get_api import ReqresGetApi
from api.reqres_post_api import ReqresPostApi

class TestAutomationPracticeTests:
    @pytest.fixture(autouse=True)
    def test_setup(self, request, page, config):
        if request.node.name == "test_valid_login_credentials" or request.node.name == "test_invalid_login_userid" or request.node.name == "test_invalid_login_password":
            self.login_page = PracticeTestAutomationLoginPage(page)
            self.login_page.open_browser(config.BASE_URL)
            return
        elif request.node.name == "test_exception_page_edit_row" or request.node.name == "test_exception_page_add_row" or request.node.name == "test_exception_page_remove_row":
            self.exception_page = PracticeTestAutomationExceptionPage(page)
            self.exception_page.open_browser(config.BASE_URL)
            return
        elif request.node.name == "test_table_page_sorting":
            self.test_table_page = PracticeTestAutomationTestTablePage(page)
            self.test_table_page.open_browser(config.BASE_URL)
            return
        elif request.node.name == "test_js_alert_handling" or request.node.name == "test_js_confirm_handling" or request.node.name == "test_js_prompt_handling":
            self.js_alert_page = JavascriptAlertHandlingPage(page)
            self.js_alert_page.open_browser()
            return
        elif request.node.name == "test_js_window_handling":
            self.js_window_page = JavascriptWindowHandlingPage(page)
            self.js_window_page.open_browser()
            return
        elif request.node.name == "test_js_frame_handling":
            self.js_frame_page = JavascriptFrameHandlingPage(page)
            self.js_frame_page.open_browser()
            return
        elif request.node.name == "test_file_upload_handling":
            self.file_upload_page = FileUploadHandlingPage(page)
            self.file_upload_page.open_browser()
            return
        elif request.node.name == "test_drag_and_drop_handling":
            self.drag_and_drop_page = DragAndDropHandlingPage(page)
            self.drag_and_drop_page.open_browser()
            return
        elif request.node.name == "test_dynamic_element_handling_hidden" or request.node.name == "test_dynamic_element_handling_rendered":
            self.dynamic_element_page = DynamicElementHandlingPage(page)
            self.dynamic_element_page.open_browser()
            return
        elif request.node.name == "test_reqres_get_api":
            self.reqres_get_api = ReqresGetApi(page, config.API_KEY)
            return
        elif request.node.name == "test_reqres_post_api":
            self.reqres_post_api = ReqresPostApi(page, config.API_KEY)
            return
        
    @pytest.mark.smoke
    def test_valid_login_credentials(self):
        self.login_page.login_with_valid_credentials()

    @pytest.mark.smoke
    def test_invalid_login_userid(self):
        self.login_page.login_with_invalid_id()

    @pytest.mark.smoke
    def test_invalid_login_password(self):
        self.login_page.login_with_invalid_password()

    @pytest.mark.smoke
    def test_exception_page_edit_row(self):
        self.exception_page.edit_row()

    @pytest.mark.smoke
    def test_exception_page_add_row(self):
        self.exception_page.add_row()   

    @pytest.mark.smoke
    def test_exception_page_remove_row(self):
        self.exception_page.remove_row()

    @pytest.mark.smoke
    def test_table_page_sorting(self):
        self.test_table_page.use_filters()

    @pytest.mark.smoke
    def test_js_alert_handling(self):
        self.js_alert_page.handle_js_alert()

    @pytest.mark.smoke
    def test_js_confirm_handling(self):
        self.js_alert_page.handle_js_confirm(accept=True)

    @pytest.mark.smoke
    def test_js_prompt_handling(self):
        self.js_alert_page.handle_js_prompt(accept=True)

    @pytest.mark.smoke
    def test_js_window_handling(self):
        self.js_window_page.handle_new_window()

    @pytest.mark.smoke
    def test_js_frame_handling(self):
        self.js_frame_page.handle_frame()

    @pytest.mark.smoke
    def test_file_upload_handling(self):
        self.file_upload_page.upload_file()

    @pytest.mark.smoke
    def test_drag_and_drop_handling(self):
        self.drag_and_drop_page.drag_and_drop_item()

    @pytest.mark.smoke
    def test_dynamic_element_handling_hidden(self):
        self.dynamic_element_page.handle_hidden_element()
    
    @pytest.mark.smoke
    def test_dynamic_element_handling_rendered(self):
        self.dynamic_element_page.handle_rendered_element()

    @pytest.mark.api
    def test_reqres_get_api(self):
        self.reqres_get_api.reqres_get_api()

    @pytest.mark.api
    def test_reqres_post_api(self):
        self.reqres_post_api.reqres_post_api()
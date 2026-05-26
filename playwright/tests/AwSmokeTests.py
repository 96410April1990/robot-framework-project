import pytest
import allure
from pages.login_page import LoginPage
from pages.home_page import HomePage

class TestAwSmokeTests:

    @pytest.fixture(autouse=True)
    def test_setup(self, request, page, config):
        if request.node.name == "test_login_with_invalid_credentials":
            self.login_page = LoginPage(page)
            self.login_page.open_browser(config.BASE_URL)
            return
        self.login_page = LoginPage(page)
        self.login_page.open_browser(config.BASE_URL)
        self.login_page.login()
        self.home_page = HomePage(page)

    @pytest.mark.smoke
    def test_asset_continue_development_feature(self):
        self.home_page.asset_continue_development_feature()

    @pytest.mark.smoke
    def test_asset_review_and_approve_feature(self):
        self.home_page.asset_review_and_approve_feature()

    @pytest.mark.smoke
    def test_integration_list_feature(self):
        self.home_page.integration_list_feature()

    @pytest.mark.smoke
    def test_login_with_invalid_credentials(self):
        self.login_page.login_with_invalid_credentials()

    @pytest.mark.smoke
    def test_development_list_feature(self):
        self.home_page.development_list_feature()

    @pytest.mark.smoke
    def test_ready_to_go_live_list_feature(self):
        self.home_page.ready_to_go_live_feature()

    @pytest.mark.smoke
    def test_snapshot_feature(self):
        self.home_page.verify_snapshot_feature()
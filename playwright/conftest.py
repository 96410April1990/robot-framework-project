import allure
import pytest

from utils.config_loader import get_config
from browser.browser_manager import BrowserManager

@pytest.fixture(scope="session")
def config():
    return get_config()

@pytest.fixture(scope="function")
def page(config):
    browser_manager = BrowserManager(config)
    page = browser_manager.launch_browser()
    yield page

    # Capture video path before context.close() finalises the file
    video_path = page.video.path() if config.RECORD_VIDEO and page.video else None

    browser_manager.close_browser()

    # Attach the finalised video to the Allure report
    if video_path:
        with open(video_path, "rb") as f:
            allure.attach(f.read(), name="Test Video", attachment_type=allure.attachment_type.WEBM)
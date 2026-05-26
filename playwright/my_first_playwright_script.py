import pytest
import allure
from playwright.sync_api import sync_playwright

@pytest.fixture()
def page():
	with sync_playwright() as p:
		browser = p.chromium.launch(
			headless=False
		)
		context = browser.new_context(
            viewport={"width": 1920, "height": 1080}, 
			record_video_dir="videos/",
			record_video_size={"width": 1280, "height": 720}
        )
		page = context.new_page()
		yield page
		video_path=page.video.path()
		context.close()
		browser.close()

		allure.attach.file(video_path, name="Test video", attachment_type=allure.attachment_type.WEBM)

def test_google(page):
		page.goto("https://www.google.com")
		page.fill("xpath=//*[@name='q']", "Playwright python")
		page.press("xpath=//*[@name='q']", "Enter")
		page.wait_for_timeout(3000)


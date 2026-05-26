from playwright.sync_api import sync_playwright

class BrowserManager:

    def __init__(self, config):
        self.config = config
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def launch_browser(self):
        self.playwright = sync_playwright().start()
        try:
            browser_type = getattr(self.playwright, self.config.BROWSER)
            self.browser = browser_type.launch(headless=self.config.HEADLESS, slow_mo=self.config.SLOW_MOTION)
            self.context = self.browser.new_context(
                viewport={"width": self.config.VIEWPORT_WIDTH, "height": self.config.VIEWPORT_HEIGHT},
                record_video_dir=self.config.VIDEO_DIR if self.config.RECORD_VIDEO else None
            )
            self.page = self.context.new_page()
            return self.page
        except Exception:
            self.playwright.stop()
            raise
    
    def close_browser(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()

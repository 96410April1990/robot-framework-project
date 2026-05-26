class BasePage:
    def __init__(self, page):
        self.page = page

    def click(self, locator):
        self.page.locator(locator).click()

    def fill(self, locator, text):
        self.page.locator(locator).fill(text)

    def get_text(self, locator):
        return self.page.locator(locator).text_content()
    
    def is_visible(self, locator):
        return self.page.locator(locator).is_visible()
    
    def wait_for_element(self, locator):
        self.page.locator(locator).wait_for()

    def hover(self, locator):
        self.page.locator(locator).hover()
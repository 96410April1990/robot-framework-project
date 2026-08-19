from utils.healing_engine import heal_and_execute

class BasePage:
    def __init__(self, page):
        self.page = page

    def click(self, locator):
        heal_and_execute(self.page, locator, "click")
        #self.page.locator(locator).click()

    def fill(self, locator, text):
        heal_and_execute(self.page, locator, "input_text", text=text)
        #self.page.locator(locator).fill(text)

    def get_text(self, locator):
        text = heal_and_execute(self.page, locator, "get_text")
        return text
        #return self.page.locator(locator).text_content()
    
    def clear_text(self, locator):
        heal_and_execute(self.page, locator, "clear_text")
        #self.page.locator(locator).fill("")
    
    def is_visible(self, locator):
        heal_and_execute(self.page, locator, "is_visible")
        return True
        # self.page.locator(locator).wait_for(state="visible", timeout=timeout)
        # return True
    
    def wait_for_element(self, locator):
        heal_and_execute(self.page, locator, "wait_for_element")
        return True
        #self.page.locator(locator).wait_for(timeout=timeout)

    def hover(self, locator):
        heal_and_execute(self.page, locator, "hover")
        #self.page.locator(locator).hover()

    def select_option(self, locator, value=None, label=None, index=None):
        heal_and_execute(self.page, locator, "select_option", value=value, label=label, index=index)
        #self.page.locator(locator).select_option(value=value, label=label, index=index)

    def accept_alert(self):
        self.page.once("dialog", lambda dialog: dialog.accept())

    def dismiss_alert(self):
        self.page.once("dialog", lambda dialog: dialog.dismiss())

    def accept_prompt(self, text: str):
        self.page.once("dialog", lambda dialog: dialog.accept(text))

    def dismiss_prompt(self, text: str):
        self.page.once("dialog", lambda dialog: dialog.dimiss(text))

    def get_alert_message(self) -> str:
        message = []
        self.page.once("dialog", lambda dialog: (message.append(dialog.message), dialog.accept()))
        return message[0] if message else ""

    def get_current_url(self):
        return self.page.url
    
    def file_upload(self, locator, file_path):
        heal_and_execute(self.page, locator, "file_upload", file_path=file_path)
        #self.page.locator(locator).set_input_files(file_path)

    def drag_and_drop(self, source_locator, target_locator):
        heal_and_execute(self.page, source_locator, "drag_and_drop", target_locator=target_locator)
        #self.page.locator(source_locator).drag_to(self.page.locator(target_locator))
        
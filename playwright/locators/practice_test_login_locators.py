class PracticeTestLoginLocators:
    LOGIN_PAGE = "//a[contains(text(),'Test Login Page')]"
    USER_NAME_INPUT = "#username"
    LOGIN_PASSWORD_INPUT = "#password"
    SIGNIN_SUBMIT_BUTTON = "xpath=//button[@id='submit']"
    INVALID_USERNAME_MSG = "xpath=//div[contains(text(),'Your username is invalid!')]"
    INVALID_PASSWORD_MSG = "xpath=//div[contains(text(),'Your password is invalid!')]"
    LOGIN_SUCCESS_MSG = "xpath=//h1[contains(text(),'Logged In Successfully')]"
    LOGIN_SUCCESS_MSG_ONE = "xpath=//strong[contains(text(),'Congratulations student. You successfully logged in!')]"
    LOGOUT_BUTTON = "xpath=//a[contains(text(),'Log out')]"



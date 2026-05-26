from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re;

def get_selenium_browser_log():
    selib = BuiltIn().get_library_instance('SeleniumLibrary')
    logs = selib.driver.get_log("performance")
    return logs

def get_capabilities_chrome():
    desiredCapability = DesiredCapabilities.CHROME
    desiredCapability['goog:loggingPrefs'] = {
    'browser': 'ALL',
    'performance' : 'ALL',
    }
    return desiredCapability;

def get_capabilities_firefox():
    desiredCapability = DesiredCapabilities.FIREFOX
    desiredCapability['goog:loggingPrefs'] = {
        'browser': 'ALL',
        'performance': 'ALL'
    }
    return desiredCapability;

def get_intake_id():
    browserlogs = get_selenium_browser_log()
    return browserlogs
    # intakeID = ''
    # for temp in browserlogs:
    #     for current in temp.keys():
    #         if current == 'intakeid':
    #            intakeID = temp['intakeid']
    #            break
    # return intakeID
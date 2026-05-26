*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${BROWSER}              Chrome
${URL}                  https://example.com
${CHROMEDRIVER_PATH}    /path/to/chromedriver
${FIREFOXDRIVER_PATH}   /path/to/geckodriver

*** Keywords ***
Set Webdriver Path
    [Arguments]    ${browser}
    Run Keyword If    '${browser}' == 'Chrome'    Set Environment Variable    webdriver.chrome.driver    ${CHROMEDRIVER_PATH}
    ...    ELSE IF    '${browser}' == 'Firefox'    Set Environment Variable    webdriver.gecko.driver     ${FIREFOXDRIVER_PATH}
    ...    ELSE    Fail    Unsupported browser: ${browser}

Open Browser With Settings
    [Arguments]    ${url}    ${browser}=${BROWSER}
    Set Webdriver Path    ${browser}
    Open Browser    ${url}    ${browser}
    Maximize Browser Window
    Set Selenium Timeout   10

Close Browser Session
    Close All Browsers

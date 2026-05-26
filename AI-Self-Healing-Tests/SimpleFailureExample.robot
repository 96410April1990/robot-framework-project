*** Settings ***
Documentation     Simple test suite with intentional failures to demonstrate AI Failure Analyzer
Library           SeleniumLibrary
Library           Collections
Suite Teardown    Close All Browsers

*** Variables ***
${BROWSER}        chrome
${TIMEOUT}        10s

*** Test Cases ***
Test Case 1: Successful Login
    [Documentation]    This test should PASS - demonstrates successful scenario
    Open Browser    https://the-internet.herokuapp.com/login    ${BROWSER}
    Wait Until Page Contains Element    id:username    timeout=${TIMEOUT}
    Input Text    id:username    tomsmith
    Input Text    id:password    SuperSecretPassword!
    Click Button    css:.fa-sign-in
    Wait Until Page Contains    You logged into a secure area!
    [Teardown]    Close Browser

Test Case 2: Wrong Selector Failure
    [Documentation]    This test should FAIL - wrong element selector
    Open Browser    https://the-internet.herokuapp.com/login    ${BROWSER}
    Wait Until Page Contains Element    id:username    timeout=${TIMEOUT}
    Input Text    id:username    tomsmith
    Input Text    id:wrong_password_id    SuperSecretPassword!    # WRONG SELECTOR
    Click Button    css:.fa-sign-in
    [Teardown]    Close Browser

Test Case 3: Timeout Failure
    [Documentation]    This test should FAIL - element doesn't exist, will timeout
    Open Browser    https://the-internet.herokuapp.com/login    ${BROWSER}
    Wait Until Page Contains Element    id:nonexistent_element    timeout=5s
    [Teardown]    Close Browser

Test Case 4: Assertion Failure
    [Documentation]    This test should FAIL - wrong expected text
    Open Browser    https://the-internet.herokuapp.com/login    ${BROWSER}
    Wait Until Page Contains Element    id:username    timeout=${TIMEOUT}
    Input Text    id:username    wronguser
    Input Text    id:password    wrongpassword
    Click Button    css:.fa-sign-in
    Wait Until Page Contains    You logged into a secure area!    # WRONG - should fail
    [Teardown]    Close Browser

Test Case 5: Missing Element After Action
    [Documentation]    This test should FAIL - clicks wrong button, next element not found
    Open Browser    https://the-internet.herokuapp.com/dropdown    ${BROWSER}
    Wait Until Page Contains Element    id:dropdown    timeout=${TIMEOUT}
    Select From List By Value    id:wrong_dropdown_id    1    # WRONG SELECTOR
    [Teardown]    Close Browser

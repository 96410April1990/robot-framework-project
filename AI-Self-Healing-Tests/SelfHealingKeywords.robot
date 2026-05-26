*** Settings ***
Documentation    Self-Healing Keywords for Robot Framework
...              This library provides self-healing capabilities for web element interactions
Library          SeleniumLibrary
Library          Collections

*** Variables ***
# Healing strategies for different element types
@{EMAIL_STRATEGIES}    id=email    id=user-email    name=email    xpath=//input[@type='email']    css=input[placeholder*='email']    css=input[type='email']
@{PASSWORD_STRATEGIES}    id=password    id=user-password    name=password    xpath=//input[@type='password']    css=input[type='password']
@{COUNTRY_STRATEGIES}    id=country    id=user-country    name=country    xpath=//select[contains(@name,'country')]    css=select[name*='country']
@{SUBMIT_STRATEGIES}    id=submit-btn    id=login-submit-button    xpath=//input[@type='submit']    xpath=//button[@type='submit']    css=button[type='submit']    xpath=//button[contains(text(),'Submit')]

*** Keywords ***
Find Element With Healing
    [Documentation]    Finds an element using multiple fallback strategies
    [Arguments]    ${element_name}    @{strategies}
    
    Log    🔍 Searching for '${element_name}' with healing...    console=True
    
    FOR    ${index}    ${strategy}    IN ENUMERATE    @{strategies}    start=1
        ${status}    Run Keyword And Return Status    Wait Until Element Is Visible    ${strategy}    timeout=2s
        IF    ${status}
            Log    ✅ Found '${element_name}' using strategy ${index}: ${strategy}    console=True
            RETURN    ${strategy}
        ELSE
            Log    ❌ Strategy ${index} failed: ${strategy}    console=True
        END
    END
    
    Fail    💥 All healing strategies failed for '${element_name}'

Heal And Input Text
    [Documentation]    Finds element with healing and inputs text
    [Arguments]    ${element_name}    ${text}    @{strategies}
    
    ${locator}    Find Element With Healing    ${element_name}    @{strategies}
    Input Text    ${locator}    ${text}
    Log    📝 Text entered in '${element_name}': ${text}    console=True

Heal And Select From List
    [Documentation]    Finds dropdown with healing and selects option
    [Arguments]    ${element_name}    ${value}    @{strategies}
    
    ${locator}    Find Element With Healing    ${element_name}    @{strategies}
    Select From List By Value    ${locator}    ${value}
    Log    🔽 Selected '${value}' in '${element_name}'    console=True

Heal And Click Element
    [Documentation]    Finds element with healing and clicks it
    [Arguments]    ${element_name}    @{strategies}
    
    ${locator}    Find Element With Healing    ${element_name}    @{strategies}
    Click Element    ${locator}
    Log    🖱️ Clicked '${element_name}'    console=True

Fill Login Form With Healing
    [Documentation]    Fills entire login form using self-healing
    [Arguments]    ${email}    ${password}    ${country}
    
    Log    🎯 Starting self-healing login form fill...    console=True
    
    # Email field with healing
    Heal And Input Text    email field    ${email}    @{EMAIL_STRATEGIES}
    
    # Password field with healing  
    Heal And Input Text    password field    ${password}    @{PASSWORD_STRATEGIES}
    
    # Country dropdown with healing
    Heal And Select From List    country dropdown    ${country}    @{COUNTRY_STRATEGIES}
    
    # Submit button with healing
    Heal And Click Element    submit button    @{SUBMIT_STRATEGIES}
    
    Log    🎉 Login form filled successfully with self-healing!    console=True
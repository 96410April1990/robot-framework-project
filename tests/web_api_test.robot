*** Settings ***
Library    RequestsLibrary
Library    SeleniumLibrary

*** Variables ***
${BROWSER}            Chrome
${BASE_URL}           https://www.google.co.in
${API_ENDPOINT}       https://jsonplaceholder.typicode.com/

*** Test Cases ***
Api And Web Automation Example
    Create Session     jsonplaceholder    ${API_ENDPOINT}   headers={}
    ${response}=       GET On Session      jsonplaceholder    posts/1
    Should Be Equal As Strings  ${response.status_code}    200
    Log  ${response.text}
    Open Browser   ${BASE_URL}    ${BROWSER}
    Sleep  3s
    ${title} =  Get Title 
    Close Browser

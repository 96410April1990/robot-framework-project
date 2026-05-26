*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    https://www.google.com
${SEARCH_TERM}    Robot Framework parallel testing

*** Test Cases ***
Google Search Test
    Open Browser    ${URL}    Chrome
    Input Text    name=q    ${SEARCH_TERM}
    Press Keys    name=q    RETURN
    Wait Until Page Contains    Robot Framework
    Close Browser

#Install the library named pabot

#pip3 install robotframework-pabot

#To run the tests in parallel, use the following command:
#pabot --processes 4 tests/RobotParallelExecutionInCiCd.robot

#To execute the same in the CI/CD pipeline, add the above command in the script section of your YAML file.


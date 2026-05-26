*** Settings ***
Library          SeleniumLibrary
Library          RequestsLibrary
Library          Collections
Library          String
Library          OperatingSystem
Suite Setup      Open Browser    about:blank    chrome
Suite Teardown   Close Browser

*** Variables ***
${WALMART_API_URL}             https://wmtllmgateway.stage.walmart.com/
${AUTHORIZATION}               Bearer eyJzZ252ZXIiOiIxIiwiYWxnIjoiSFMyNTYiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIxMTA5MiIsInN1YiI6IjE3IiwiaXNzIjoiV01UTExNR0FURVdBWS1TVEciLCJhY3QiOiJyMG4wMWd1IiwidHlwZSI6IlVTUiIsImlhdCI6MTc2ODkxNzU2MiwiZXhwIjoxNzc0MTAxNTYyfQ.n9lfkbdUjrkNQEit3VxUGoTBKMLrFsJw6eELs05zMZ4
${CONTENT_TYPE}                application/json
${CONSUMER_ID}                 SelfHealingFramework-QA
${SERVICE_ENV}                 stage
${SERVICE_NAME}                WMTLLMGATEWAY
${USER_AGENT}                  SelfHealingFramework-QA/1.0
${MAX_TOKENS}                  150
${TEMPERATURE}                 0.1
${TIMEOUT}                     30

*** Test Cases ***
Open Google.com And Find Element Locators Using Ai To Click Element And Send Keys
    [Documentation]    Test case to open Google.com and find element locators using AI to click element and send keys
    Go To  https://www.google.com
    Sleep  5s
    ${page_source} =      Get Source
    ${page_title} =       Get Title
    ${page_current_url} =   Get Location
    Log  Page Source: ${page_source}
    Log  Page Title: ${page_title}
    Log  Page Current URL: ${page_current_url}
    
    # Create AI prompt as a single string using Catenate
    ${ai_prompt_input_field} =  Catenate    SEPARATOR=\n
    ...    You are a web automation expert. Analyze this HTML page and suggest 3-5 CSS selectors or XPath expressions to find a search input field.
    ...    ${EMPTY}
    ...    Page Context:
    ...    - URL: ${page_current_url}
    ...    - Title: ${page_title}
    ...    - Task: Find search input field
    ...    ${EMPTY}
    ...    HTML Source:
    ...    ${page_source}
    ...    ${EMPTY}
    ...    Return only the selectors, one per line, in order of reliability. Use formats like:
    ...    id=element-id
    ...    css=.class-name
    ...    xpath=//element[@attribute='value']
    
    # Create content object with prompt as string (GPT-4o multimodal format)
    ${text_content} =  Create Dictionary  type=text  text=${ai_prompt_input_field}
    ${content_array} =  Create List  ${text_content}
    
    ${messages} =  Create List
    ${msg} =  Create Dictionary  role=user  content=${content_array}
    Append To List  ${messages}  ${msg}

    # Convert max_tokens and temperature to proper numeric types
    ${max_tokens_int} =  Convert To Integer  ${MAX_TOKENS}
    ${temperature_float} =  Convert To Number  ${TEMPERATURE}

    ${body} =  Create Dictionary
    ...    messages=${messages}
    ...    max_tokens=${max_tokens_int}
    ...    temperature=${temperature_float}
    
    ${headers} =  Create Dictionary
    ...    Authorization=${AUTHORIZATION}
    ...    Content-Type=${CONTENT_TYPE}
    ...    consumer-id=${CONSUMER_ID}
    ...    service-env=${SERVICE_ENV}
    ...    service-name=${SERVICE_NAME}
    ...    User-Agent=${USER_AGENT}
    
    Create Session  openai  ${WALMART_API_URL}  verify=False
    
    ${response} =  Post Request
    ...    openai
    ...    wmtllmgateway/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview
    ...    headers=${headers}
    ...    json=${body}
    
    # Log the full response for debugging
    Log    Response Status: ${response.status_code}    console=True
    Log    Response Body: ${response.json()}    console=True
    
    # Check if response has choices before accessing
    ${response_json} =  Set Variable  ${response.json()}
    ${has_choices} =  Run Keyword And Return Status    Dictionary Should Contain Key    ${response_json}    choices
    
    IF    ${has_choices}
        ${answer} =  Set Variable  ${response_json["choices"][0]["message"]["content"]}
        Log    AI Response: ${answer}    console=True
        # Parse the response to extract selectors (remove code block markers if present)
        ${cleaned_response} =  Replace String    ${answer}    ```plaintext    ${EMPTY}
        ${cleaned_response} =  Replace String    ${cleaned_response}    ```    ${EMPTY}
        ${cleaned_response} =  Strip String      ${cleaned_response}

        # Split into lines to get individual selectors
        @{selector_lines} =  Split To Lines    ${cleaned_response}

        # Get the first selector (most reliable according to AI)
        ${first_selector} =  Set Variable    ${selector_lines}[0]
        ${first_selector} =  Strip String     ${first_selector}

        Log    🎯 Using first selector: ${first_selector}    console=True

        # Now use this selector to interact with the element
        Input Text    ${first_selector}   Rohith Nandakumar
        Sleep  10s
    ELSE
        Log    API Error Response: ${response_json}    console=True
        Fail    API returned error: ${response_json}
    END

    ${ai_prompt_search_button} =  Catenate    SEPARATOR=\n
    ...    You are a web automation expert. Analyze this HTML page and suggest 3-5 CSS selectors or XPath expressions to find the search button.
    ...    ${EMPTY}
    ...    Page Context:
    ...    - URL: ${page_current_url}
    ...    - Title: ${page_title}
    ...    - Task: Find search button
    ...    ${EMPTY}
    ...    HTML Source:
    ...    ${page_source}
    ...    ${EMPTY}
    ...    Return only the selectors, one per line, in order of reliability. Use formats like:
    ...    id=element-id
    ...    css=.class-name
    ...    xpath=//element[@attribute='value']
    
    ${text_content} =  Create Dictionary  type=text  text=${ai_prompt_search_button}
    ${content_array} =  Create List  ${text_content}
    
    ${messages} =  Create List
    ${msg} =  Create Dictionary  role=user  content=${content_array}
    Append To List  ${messages}  ${msg}

    # Convert max_tokens and temperature to proper numeric types
    ${max_tokens_int} =  Convert To Integer  ${MAX_TOKENS}
    ${temperature_float} =  Convert To Number  ${TEMPERATURE}

    ${body} =  Create Dictionary
    ...    messages=${messages}
    ...    max_tokens=${max_tokens_int}
    ...    temperature=${temperature_float}
    
    ${headers} =  Create Dictionary
    ...    Authorization=${AUTHORIZATION}
    ...    Content-Type=${CONTENT_TYPE}
    ...    consumer-id=${CONSUMER_ID}
    ...    service-env=${SERVICE_ENV}
    ...    service-name=${SERVICE_NAME}
    ...    User-Agent=${USER_AGENT}
    
    Create Session  openai  ${WALMART_API_URL}  verify=False
    
    ${response} =  Post Request
    ...    openai
    ...    wmtllmgateway/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview
    ...    headers=${headers}
    ...    json=${body}
    
    # Log the full response for debugging
    Log    Response Status: ${response.status_code}    console=True
    Log    Response Body: ${response.json()}    console=True
    
*** Keywords ***


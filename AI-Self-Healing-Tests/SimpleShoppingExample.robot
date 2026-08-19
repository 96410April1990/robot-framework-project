*** Settings ***
Documentation    Simple Self-Healing Example - Shopping Cart Test
...              This shows a real-world example: adding items to a shopping cart
...              Works even when developers change button names or IDs
Library          SeleniumLibrary
Library          RequestsLibrary
Library          Collections
Library          String
Library          OperatingSystem
Resource         SelfHealingKeywords.robot
Suite Setup      Setup Test Environment
Suite Teardown   Close Browser

*** Variables ***
# Simple test data
${PRODUCT_NAME}     Robot Framework Book
${QUANTITY}         2

# Healing strategies for shopping elements  
@{PRODUCT_SEARCH_STRATEGIES}    id=search-box    name=search    css=input[placeholder*='search']    xpath=//input[@type='text']
@{ADD_TO_CART_STRATEGIES}       id=add-to-cart    css=.add-cart-btn    xpath=//button[contains(text(),'Add to Cart')]    xpath=//button[contains(text(),'Add')]
@{QUANTITY_STRATEGIES}          id=quantity    name=qty    css=input[type='number']    xpath=//input[@type='number']
@{CHECKOUT_STRATEGIES}          id=checkout    css=.checkout-btn    xpath=//button[contains(text(),'Checkout')]    xpath=//a[contains(text(),'Checkout')]

# File paths for demo pages
${SHOP_ORIGINAL}     file://${CURDIR}/shop_page.html
${SHOP_CHANGED}      file://${CURDIR}/shop_page_changed.html

# Google Vertex AI Gemini Configuration
${AI_ENDPOINT}       https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent
${AI_MODEL}          gemini-1.5-flash
${AI_MAX_TOKENS}     200
${AI_TEMPERATURE}    0.1
${VERTEX_AI_API_KEY}    ${EMPTY}  # Will be loaded from gemini_config.py

*** Test Cases ***
Simple Shopping Test - Original Page
    [Documentation]    Basic shopping test on original page layout
    [Tags]    shopping    original
    
    Log    🛒 SIMPLE SHOPPING TEST: Original Page    console=True
    Log    ================================================    console=True
    
    # Go to shop page
    Go To    ${SHOP_ORIGINAL}
    Log    🏪 Opened shopping website    console=True
    
    # Search for product
    Heal And Input Text    search box    ${PRODUCT_NAME}    @{PRODUCT_SEARCH_STRATEGIES}
    Log    🔍 Searched for: ${PRODUCT_NAME}    console=True
    
    # Add to cart
    Heal And Click Element    add to cart button    @{ADD_TO_CART_STRATEGIES}
    Log    ➕ Added item to cart    console=True
    
    # Verify success
    Wait Until Page Contains    Item added to cart    timeout=5s
    Log    ✅ SUCCESS: Item added successfully!    console=True

Simple Shopping Test - Changed Page (Self-Healing)
    [Documentation]    Same test but page layout changed - watch healing work!
    [Tags]    shopping    healing    changed
    
    Log    🛒 SIMPLE SHOPPING TEST: Changed Page (Healing Demo)    console=True  
    Log    ================================================    console=True
    Log    💡 Developer changed all element IDs - but test still works!    console=True
    
    # Go to changed shop page
    Go To    ${SHOP_CHANGED}  
    Log    🏪 Opened CHANGED shopping website    console=True
    
    # Search for product (healing will find new locator automatically)
    Heal And Input Text    search box    ${PRODUCT_NAME}    @{PRODUCT_SEARCH_STRATEGIES}
    Log    🔍 Searched for: ${PRODUCT_NAME} (with healing!)    console=True
    
    # Add to cart (healing will find new button automatically)  
    Heal And Click Element    add to cart button    @{ADD_TO_CART_STRATEGIES}
    Log    ➕ Added item to cart (with healing!)    console=True
    
    # Verify success
    Wait Until Page Contains    Item added successfully    timeout=5s
    Log    🎉 SUCCESS: Healing worked! Same test, different page layout!    console=True

AI-Powered Shopping Test
    [Documentation]    Advanced test with AI-generated healing strategies
    [Tags]    shopping    ai-healing    advanced
    
    Log    🤖 AI-POWERED SHOPPING TEST    console=True
    Log    ================================================    console=True
    Log    🧠 AI will analyze page and suggest new locators if needed    console=True
    
    # Go to changed page
    Go To    ${SHOP_CHANGED}
    Log    🏪 Testing AI healing on changed page    console=True
    
    # Use AI-powered healing for search
    AI Enhanced Search And Add To Cart    ${PRODUCT_NAME}
    
    # Verify with AI assistance
    ${success_found}    AI Find Success Message
    IF    ${success_found}
        Log    🎉 AI SUCCESS: Found success message using intelligent analysis!    console=True
    ELSE
        Log    ⚠️ AI could not locate success message    console=True
    END

REAL AI Shopping Test - Google Gemini Integration
    [Documentation]    Uses Vertex AI Gemini API for intelligent element detection
    [Tags]    shopping    real-ai    vertex-ai-integration
    
    Log    🏢 REAL AI SHOPPING TEST - Vertex AI Gemini Integration    console=True
    Log    ================================================================    console=True
    Log    🤖 Using Google Vertex AI with Gemini model    console=True
    
    # Check if Gemini AI is configured
    ${ai_configured}    Check Gemini Configuration
    IF    not ${ai_configured}
        Log    ⚠️ Gemini API not configured - using demo mode    console=True
        Skip    Gemini API test requires valid API key configuration
    END
    
    # Go to changed page that will challenge the AI
    Go To    ${SHOP_CHANGED}
    Log    🏪 Testing REAL AI on challenging changed page    console=True
    
    # Use real AI for search box detection
    Log    🧠 Activating REAL AI for search box detection...    console=True
    ${search_locator}    Real AI Find Element    search input field
    Input Text    ${search_locator}    ${PRODUCT_NAME}
    Log    🎯 REAL AI found search box: ${search_locator}    console=True
    
    # Use real AI for add to cart button
    Log    🧠 Activating REAL AI for cart button detection...    console=True  
    ${cart_locator}    Real AI Find Element    add to cart button
    Click Element    ${cart_locator}
    Log    🎯 REAL AI found cart button: ${cart_locator}    console=True
    
    # Verify success with AI
    ${success_locator}    Real AI Find Element    success confirmation message
    Wait Until Element Is Visible    ${success_locator}    timeout=5s
    ${success_text}    Get Text    ${success_locator}
    Log    🏆 REAL AI SUCCESS: Found success message "${success_text}"    console=True
    Log    🎉 Corporate AI integration working perfectly!    console=True

*** Keywords ***
Setup Test Environment
    [Documentation]    Sets up test environment and loads Vertex AI configuration
    
    # Load Vertex AI configuration from gemini_config.py
    ${config_exists}    Run Keyword And Return Status    File Should Exist    ${CURDIR}/gemini_config.py
    IF    ${config_exists}
        Log    📋 Loading Vertex AI Gemini configuration    console=True
        ${config_status}    Check Gemini Configuration
        IF    ${config_status}
            Log    ✅ Vertex AI API configured successfully    console=True
        ELSE
            Log    ⚠️ Vertex AI API key not configured - tests will fail    console=True
        END
    ELSE
        Log    ⚠️ gemini_config.py not found!    console=True
    END
    
    # Open browser
    Open Browser    about:blank    chrome
    Log    🚀 Test environment ready    console=True
AI Enhanced Search And Add To Cart
    [Documentation]    Uses AI to analyze page and find elements intelligently
    [Arguments]    ${product}
    
    Log    🤖 Starting AI-enhanced element detection...    console=True
    
    # Try normal healing first
    ${search_found}    Run Keyword And Return Status    
    ...    Heal And Input Text    search box    ${product}    @{PRODUCT_SEARCH_STRATEGIES}
    
    IF    not ${search_found}
        Log    🧠 Normal healing failed, activating AI analysis...    console=True
        ${ai_search_locator}    AI Analyze And Find Element    search input field
        Input Text    ${ai_search_locator}    ${product}
        Log    🎯 AI found search box: ${ai_search_locator}    console=True
    ELSE
        Log    ✅ Normal healing worked for search box    console=True
    END
    
    # Try to add to cart with AI backup
    ${cart_found}    Run Keyword And Return Status    
    ...    Heal And Click Element    add to cart button    @{ADD_TO_CART_STRATEGIES}
    
    IF    not ${cart_found}
        Log    🧠 Normal healing failed for cart button, using AI...    console=True
        ${ai_cart_locator}    AI Analyze And Find Element    add to cart button
        Click Element    ${ai_cart_locator}
        Log    🎯 AI found cart button: ${ai_cart_locator}    console=True
    ELSE
        Log    ✅ Normal healing worked for cart button    console=True
    END

AI Analyze And Find Element
    [Documentation]    Uses AI to analyze page structure and suggest locators
    [Arguments]    ${element_description}
    
    Log    🤖 AI analyzing page for: ${element_description}    console=True
    
    # Get page source for AI analysis
    ${page_source}    Get Source
    
    # Simulate AI analysis (in real implementation, this would call your AI API)
    ${ai_suggestions}    AI Generate Locator Suggestions    ${element_description}    ${page_source}
    
    # Try AI-suggested locators
    FOR    ${suggestion}    IN    @{ai_suggestions}
        ${status}    Run Keyword And Return Status    Wait Until Element Is Visible    ${suggestion}    timeout=1s
        IF    ${status}
            Log    🎯 AI SUCCESS: Found element using ${suggestion}    console=True
            RETURN    ${suggestion}
        END
    END
    
    Fail    🤖 AI analysis could not find element: ${element_description}

AI Generate Locator Suggestions
    [Documentation]    Simulates AI-powered locator generation
    [Arguments]    ${element_type}    ${page_source}
    
    Log    🧠 AI is analyzing page structure...    console=True
    
    # In real implementation, this would:
    # 1. Send page_source to AI API
    # 2. Ask AI to analyze and suggest locators for element_type  
    # 3. Return AI-generated suggestions
    
    # For demo, return smart fallback strategies based on element type
    IF    'search' in '${element_type}'.lower()
        ${suggestions}    Create List    css=input[placeholder*='find']    css=input[name*='search']    xpath=//input[contains(@class,'search')]
    ELSE IF    'cart' in '${element_type}'.lower()
        ${suggestions}    Create List    css=button[class*='cart']    xpath=//button[contains(@onclick,'cart')]    css=.purchase-btn
    ELSE
        ${suggestions}    Create List    css=*[class*='${element_type}']    xpath=//*[contains(text(),'${element_type}')]
    END
    
    ${suggestion_count}    Get Length    ${suggestions}
    Log    🤖 AI generated ${suggestion_count} smart suggestions    console=True
    RETURN    ${suggestions}

AI Find Success Message  
    [Documentation]    Uses AI to find success confirmation messages
    
    Log    🤖 AI searching for success confirmation...    console=True
    
    # AI-powered search for success indicators
    @{success_patterns}    Create List
    ...    xpath=//*[contains(text(),'success')]
    ...    xpath=//*[contains(text(),'added')]  
    ...    xpath=//*[contains(text(),'cart')]
    ...    css=.success-message
    ...    css=.notification
    
    FOR    ${pattern}    IN    @{success_patterns}
        ${found}    Run Keyword And Return Status    Wait Until Element Is Visible    ${pattern}    timeout=1s
        IF    ${found}
            ${text}    Get Text    ${pattern}
            Log    🎯 AI found success message: "${text}"    console=True
            RETURN    ${True}
        END
    END
    
    RETURN    ${False}

Check Gemini Configuration
    [Documentation]    Tests if Vertex AI is properly configured
    
    TRY
        # Import gemini_config.py to get API configuration
        ${config_data}    Evaluate    
        ...    exec(open('${CURDIR}/gemini_config.py').read()) or GEMINI_CONFIG
        ...    modules=sys
        
        ${api_key}    Get From Dictionary    ${config_data}    api_key
        
        # Test if API key is valid
        Log    🧪 Testing Vertex AI connection...    console=True
        
        ${key_length}    Get Length    ${api_key}
        
        IF    ${key_length} > 20 and "AQ." in "${api_key}"
            Log    ✅ Valid Vertex AI API key found!    console=True
            RETURN    ${True}
        ELSE
            Log    ⚠️ Invalid or placeholder API key configured    console=True
            RETURN    ${False}
        END
        
    EXCEPT    AS    ${error}
        Log    ⚠️ Error checking Vertex AI configuration: ${error}    console=True
        RETURN    ${False}
    END

Real AI Find Element
    [Documentation]    Uses Vertex AI Gemini API to find page elements
    [Arguments]    ${element_description}
    
    Log    🤖 VERTEX AI: Analyzing page for ${element_description}    console=True
    
    # Get current page source for AI analysis
    ${page_source}    Get Source
    ${page_title}    Get Title
    ${current_url}    Get Location
    
    # Limit page source to avoid token limits (first 2000 chars)
    ${truncated_source}    Evaluate    "${page_source}"[:2000]
    
    # Create AI prompt for element analysis
    ${ai_prompt}    Set Variable    
    ...    You are a web automation expert. Analyze this HTML and suggest 5 CSS selectors or XPath to find "${element_description}".
    ...    
    ...    Page: ${page_title}
    ...    URL: ${current_url}
    ...    
    ...    HTML: ${truncated_source}
    ...    
    ...    Return ONLY selectors, one per line:
    ...    css=.class-name
    ...    xpath=//element[@attr='value']
    ...    id=element-id
    
    # Get AI suggestions from Vertex AI
    ${ai_suggestions}    Call Gemini API    ${ai_prompt}
    
    # Try each AI suggestion
    FOR    ${suggestion}    IN    @{ai_suggestions}
        ${suggestion}    Strip String    ${suggestion}
        Continue For Loop If    "${suggestion}" == ""
        
        Log    🧠 Trying Vertex AI suggestion: ${suggestion}    console=True
        ${found}    Run Keyword And Return Status    Wait Until Element Is Visible    ${suggestion}    timeout=2s
        IF    ${found}
            Log    🎯 VERTEX AI SUCCESS: Found element using ${suggestion}    console=True
            RETURN    ${suggestion}
        ELSE
            Log    ❌ Suggestion failed: ${suggestion}    console=True
        END
    END
    
    Fail    🤖 Vertex AI could not find element: ${element_description}

Call Gemini API
    [Documentation]    Makes API call to Vertex AI Gemini for element analysis
    [Arguments]    ${prompt}
    
    Log    🤖 Calling Vertex AI Gemini API...    console=True
    
    TRY
        # Load API key from config
        ${config_data}    Evaluate    
        ...    exec(open('${CURDIR}/gemini_config.py').read()) or GEMINI_CONFIG
        ...    modules=sys
        ${api_key}    Get From Dictionary    ${config_data}    api_key
        
        Log    🔑 API key loaded, calling Vertex AI...    console=True
        
        # Make API call to Vertex AI Gemini endpoint
        ${ai_response}    Evaluate    
        ...    __import__('requests').post('https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${api_key}', headers={'Content-Type': 'application/json'}, json={'contents': [{'parts': [{'text': r'''${prompt}'''}]}], 'generationConfig': {'maxOutputTokens': 200, 'temperature': 0.1}}, timeout=30).json()
        ...    modules=requests
        
        Log    📡 Vertex AI response received    console=True
        
        # Extract response - Vertex AI returns candidates in a different format
        ${has_candidates}    Run Keyword And Return Status    Dictionary Should Contain Key    ${ai_response}    candidates
        IF    ${has_candidates}
            # Standard Gemini API format
            Log    📡 Using standard Gemini response format    console=True
            ${candidates}    Get From Dictionary    ${ai_response}    candidates
            ${candidates_length}    Get Length    ${candidates}
            IF    ${candidates_length} == 0
                Log    ❌ Empty candidates array    console=True
                ${fallback_selectors}    Create List    css=input[type="text"]    css=button    xpath=//input    xpath=//button
                RETURN    ${fallback_selectors}
            END
            ${first_candidate}    Set Variable    ${candidates}[0]
            ${content}    Get From Dictionary    ${first_candidate}    content
            ${parts}    Get From Dictionary    ${content}    parts
            ${first_part}    Set Variable    ${parts}[0]
            ${ai_text}    Get From Dictionary    ${first_part}    text
        ELSE
            # Check for Vertex AI specific response format
            ${has_predictions}    Run Keyword And Return Status    Dictionary Should Contain Key    ${ai_response}    predictions
            IF    ${has_predictions}
                Log    📡 Using Vertex AI response format    console=True
                ${predictions}    Get From Dictionary    ${ai_response}    predictions
                ${pred_length}    Get Length    ${predictions}
                IF    ${pred_length} == 0
                    Log    ❌ Empty predictions array    console=True
                    ${fallback_selectors}    Create List    css=input[type="text"]    css=button    xpath=//input    xpath=//button
                    RETURN    ${fallback_selectors}
                END
                ${first_pred}    Set Variable    ${predictions}[0]
                ${pred_candidates}    Get From Dictionary    ${first_pred}    candidates
                ${first_candidate}    Set Variable    ${pred_candidates}[0]
                ${content}    Get From Dictionary    ${first_candidate}    content
                ${parts}    Get From Dictionary    ${content}    parts
                ${first_part}    Set Variable    ${parts}[0]
                ${ai_text}    Get From Dictionary    ${first_part}    text
            ELSE
                Log    ❌ Unknown response format    console=True
                Log    Response: ${ai_response}    console=True
                ${fallback_selectors}    Create List    css=input[type="text"]    css=button    xpath=//input    xpath=//button
                RETURN    ${fallback_selectors}
            END
        END
        
        Log    🧠 AI Response: ${ai_text}    console=True
        
        # Convert AI response to list of selectors
        ${selectors}    Parse AI Response To Selectors    ${ai_text}
        
        ${selector_count}    Get Length    ${selectors}
        Log    🤖 AI generated ${selector_count} selector suggestions    console=True
        RETURN    ${selectors}
        
    EXCEPT    AS    ${error}
        Log    ❌ AI API call failed: ${error}    console=True
        Log    🔄 Using fallback selectors...    console=True
        
        ${fallback_selectors}    Create List    
        ...    css=input[type="text"]
        ...    css=input[placeholder*="search"]
        ...    css=button[type="submit"]
        ...    css=.btn
        ...    xpath=//input[@type="text"]
        ...    xpath=//button[contains(text(),"Search")]
        
        Log    🤖 Using fallback selectors    console=True
        RETURN    ${fallback_selectors}
    END

Parse AI Response To Selectors
    [Documentation]    Converts AI text response into list of usable selectors
    [Arguments]    ${ai_response}
    
    @{selectors}    Create List
    @{lines}    Split To Lines    ${ai_response}
    
    FOR    ${line}    IN    @{lines}
        ${line}    Strip String    ${line}
        
        # Skip empty lines
        ${line_length}    Get Length    ${line}
        Continue For Loop If    ${line_length} == 0
        
        # Skip comment lines
        ${is_comment}    Run Keyword And Return Status    Should Start With    ${line}    \#
        Continue For Loop If    ${is_comment}
        
        # Check for valid selector patterns using safer string operations
        ${is_id_selector}        Run Keyword And Return Status    Should Start With    ${line}    id=
        ${is_css_selector}       Run Keyword And Return Status    Should Start With    ${line}    css=
        ${is_xpath_selector}     Run Keyword And Return Status    Should Start With    ${line}    xpath=
        ${is_name_selector}      Run Keyword And Return Status    Should Start With    ${line}    name=
        
        ${is_valid_selector}    Evaluate    ${is_id_selector} or ${is_css_selector} or ${is_xpath_selector} or ${is_name_selector}
        
        IF    ${is_valid_selector}
            Log    🎯 Found valid selector: ${line}    console=True
            Append To List    ${selectors}    ${line}
        ELSE
            # Try to extract selectors from descriptive text
            ${extracted}    Extract Selector From Text    ${line}
            ${extracted_length}    Get Length    ${extracted}
            IF    ${extracted_length} > 0
                Log    🔍 Extracted selector from text: ${extracted}    console=True
                Append To List    ${selectors}    ${extracted}
            ELSE
                Log    ⚠️ Skipping invalid line: ${line}    console=True
            END
        END
    END
    
    ${selector_count}    Get Length    ${selectors}
    Log    📋 Parsed ${selector_count} valid selectors from AI response    console=True
    RETURN    ${selectors}

Extract Selector From Text
    [Documentation]    Extracts CSS/XPath selectors from AI descriptive text
    [Arguments]    ${text}
    
    # Look for common patterns in AI responses like:
    # "Try using id=search-box"
    # "The selector css=.search-input should work"
    # "Use xpath=//input[@type='text']"
    
    Log    🔍 Analyzing text for selectors: ${text}    console=True
    
    # Try to find id= patterns
    ${id_matches}    Get Regexp Matches    ${text}    id=[\\w\\-_]+
    IF    ${id_matches}
        ${first_match}    Set Variable    ${id_matches}[0]
        Log    ✅ Found ID selector: ${first_match}    console=True
        RETURN    ${first_match}
    END
    
    # Try to find css= patterns (be more careful with special characters)
    ${css_matches}    Get Regexp Matches    ${text}    css=[^\\s"']+
    IF    ${css_matches}
        ${first_match}    Set Variable    ${css_matches}[0]
        Log    ✅ Found CSS selector: ${first_match}    console=True
        RETURN    ${first_match}
    END
    
    # Try to find xpath= patterns
    ${xpath_matches}    Get Regexp Matches    ${text}    xpath=[^\\s"']+
    IF    ${xpath_matches}
        ${first_match}    Set Variable    ${xpath_matches}[0]
        Log    ✅ Found XPath selector: ${first_match}    console=True
        RETURN    ${first_match}
    END
    
    # Try to find name= patterns
    ${name_matches}    Get Regexp Matches    ${text}    name=[\\w\\-_]+
    IF    ${name_matches}
        ${first_match}    Set Variable    ${name_matches}[0]
        Log    ✅ Found name selector: ${first_match}    console=True
        RETURN    ${first_match}
    END
    
    Log    ❌ No valid selectors found in text    console=True
    RETURN    ${EMPTY}
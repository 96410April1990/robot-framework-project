*** Settings ***
Documentation    Self-Healing Robot Framework Test Example
...              This demonstrates how to write tests that heal themselves when elements change
Library          SeleniumLibrary
Resource         SelfHealingKeywords.robot
Suite Setup      Open Browser    about:blank    chrome
Suite Teardown   Close Browser

*** Variables ***
${TEST_EMAIL}        test@example.com
${TEST_PASSWORD}     password123
${TEST_COUNTRY}      us

# File paths for test pages
${ORIGINAL_PAGE}     file://${CURDIR}/test_page.html
${CHANGED_PAGE}      file://${CURDIR}/test_page_changed.html

*** Test Cases ***
Test Original Page With Self Healing
    [Documentation]    Test the original page using self-healing keywords
    [Tags]    self-healing    original-page
    
    Log    🧪 TESTING: Original Page with Self-Healing    console=True
    Log    ============================================================    console=True
    
    # Navigate to original page
    Go To    ${ORIGINAL_PAGE}
    Log    📂 Loaded original page    console=True
    
    # Fill form using self-healing keywords
    Fill Login Form With Healing    ${TEST_EMAIL}    ${TEST_PASSWORD}    ${TEST_COUNTRY}
    
    # Verify success message appears
    Wait Until Element Is Visible    id=success-message    timeout=5s
    Element Should Be Visible    id=success-message
    Log    ✅ SUCCESS: Original page test completed!    console=True

Test Changed Page With Self Healing
    [Documentation]    Test the changed page using self-healing keywords - this is where healing magic happens!
    [Tags]    self-healing    changed-page
    
    Log    🧪 TESTING: Changed Page with Self-Healing    console=True
    Log    ============================================================    console=True
    Log    💡 This page has different element IDs - watch the healing work!    console=True
    
    # Navigate to changed page
    Go To    ${CHANGED_PAGE}
    Log    📂 Loaded changed page (with different element IDs)    console=True
    
    # Fill form using same self-healing keywords
    Fill Login Form With Healing    ${TEST_EMAIL}    ${TEST_PASSWORD}    ${TEST_COUNTRY}
    
    # Verify success message appears (also has changed ID)
    ${success_locator}    Find Element With Healing    success message    id=success-message    id=login-success-notification
    Wait Until Element Is Visible    ${success_locator}    timeout=5s
    Element Should Be Visible    ${success_locator}
    Log    🎉 SUCCESS: Changed page test completed with healing!    console=True

Compare Normal vs Self Healing Test
    [Documentation]    Demonstrates the difference between normal and self-healing approaches
    [Tags]    comparison    demo
    
    Log    📊 COMPARISON: Normal vs Self-Healing Approach    console=True
    Log    ============================================================    console=True
    
    # Test normal approach on changed page (will fail)
    Go To    ${CHANGED_PAGE}
    Log    🔴 Trying NORMAL approach (should fail)...    console=True
    
    ${status}    Run Keyword And Return Status    Input Text    id=email    ${TEST_EMAIL}
    IF    not ${status}
        Log    ❌ NORMAL approach FAILED: Element 'id=email' not found    console=True
    END
    
    # Test self-healing approach on same page (will succeed)
    Log    🟢 Trying SELF-HEALING approach (should succeed)...    console=True
    Fill Login Form With Healing    ${TEST_EMAIL}    ${TEST_PASSWORD}    ${TEST_COUNTRY}
    
    # Verify success
    ${success_locator}    Find Element With Healing    success message    id=success-message    id=login-success-notification
    Wait Until Element Is Visible    ${success_locator}    timeout=5s
    Log    🎯 RESULT: Self-healing succeeded where normal approach failed!    console=True

*** Keywords ***
# You can add more custom keywords here for your specific application
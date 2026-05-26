import playwright
import time
import pytest
import allure
import json
import os
from playwright.sync_api import sync_playwright
from faker import Faker

@pytest.fixture()
def browser_launch():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            channel="chrome"
        )
        context = browser.new_context(
            viewport = {"width": 1920, "height": 1080},
            record_video_dir = "videos/",
            record_video_size = {"width": 1280, "height": 720}
        )
        page = context.new_page()
        yield page, context, p
        video_path = page.video.path()
        context.close()
        browser.close()
        allure.attach.file(video_path, name = "CPRA Intake Access Reject Test", attachment_type = allure.attachment_type.WEBM)

def test_cpra_intake_access_reject_flow(browser_launch):
    page, context, p = browser_launch
    intake_request_id = None
    # Event listener to capture intake ID
    def handle_response_headers(response):
        nonlocal intake_request_id
        headers = response.headers
        print("Response headers:", headers)  # Debugging line to print all response headers
        if "x-dc-wm_intakeid" in headers:
            intake_request_id = headers["x-dc-wm_intakeid"]
            print(f"Captured Intake Request ID: {intake_request_id}")
    context.on("response", handle_response_headers)
    page.goto("https://cpa-ui-qa.walmart.com/affirmation?brandCode=WMTSC&requestType=optout&languageCode=en-GSE_US&market=GSE")
    home_page_title = page.title()
    expected_home_page_title = "Who is making the request and are they a CA resident?"
    if home_page_title == expected_home_page_title:
        print("Successfully navigated to the CPRA Intake form")
    else:
        print("Failed to navigate to the CPRA Intake form")
    page.click("#state")
    page.select_option("#state", "California")
    page.click("#requestFor")
    page.select_option("#requestFor", "Myself")
    page.click("xpath=//span[contains(text(),'Yes')]")
    page.click("xpath=//button[contains(text(),'Create privacy request')]")

    otp_page_title = page.title()
    expected_otp_page_title = "Email Verification"
    if otp_page_title == expected_otp_page_title:
        print("Successfully navigated to the OTP verification page")
    else:
        print("Failed to navigate to the OTP verification page")

    fake = Faker()
    first_name = fake.first_name()
    email_id = f"{first_name.lower()}@getnada.com"
    phone_number = fake.msisdn()[:10]

    page.click("#email")
    page.fill("#email", email_id)
    page.click("xpath=//button[contains(text(),'Get Code')]")

    for i in range(30):
        if intake_request_id:
            break
        time.sleep(3)
    else:
        print("Failed to capture Intake Request ID from response headers")
        page.close()
        return
    
    print(f"Using Intake Request ID: {intake_request_id} to fetch OTP from email")
    otp_api_request = p.request.new_context(extra_http_headers={"X-WM-DC.TRACE.TENANT_ID": "GSE"})
    otp_api_response = otp_api_request.get(f"http://cpa-otp-qa.walmart.com/v1/otp/test?guid={intake_request_id}&brandCode=WMTSC&emailId={email_id}")
    print("OTP api response status:", otp_api_response.status)

    try:
        response_json = otp_api_response.json()
        if otp_api_response.status == 200 and "otp" in response_json:
            otp = response_json["otp"]
            print(f"OTP captured: {otp}")    
        else:
            print(f"OTP API failed with status {otp_api_response.status}")
            otp_api_request.dispose()
            page.close()
            return
    except Exception as e:
        print(f"OTP parsing error: {str(e)}")
        otp_api_request.dispose()
        page.close()
        return

    otp_api_request.dispose()

    page.click("#otp")
    page.fill("#otp", f"{otp}")
    page.click("xpath=//button[contains(text(),'Continue')]")

    request_selection_page_title = page.title()
    expected_request_selection_page_title = "Request Selection"
    if request_selection_page_title == expected_request_selection_page_title:
        print("Successfully navigated to the Request Selection page")
    else:   
        print("Failed to navigate to the Request Selection page")
    
    page.click("xpath=//div[contains(text(),'Access')]")
    page.click("xpath=//button[contains(text(),'Proceed')]")

    irr_page_title = page.title()
    expected_irr_page_title = "Request for your information"
    if irr_page_title == expected_irr_page_title:
        print("Successfully navigated to the Request for your information page")
    else:
        print("Failed to navigate to the Request for your information page")

    page.click("xpath=//input[@id='firstName']")
    page.fill("xpath=//input[@id='firstName']", first_name)
    page.click("xpath=//input[@id='lastName']")
    page.fill("xpath=//input[@id='lastName']", 'perftest')
    page.select_option("#phoneCountryCode", "IN : +91")
    page.click("xpath=//input[@id='phoneNumber']")
    page.fill("xpath=//input[@id='phoneNumber']", phone_number)  # Unique phone per user
    page.click("xpath=//input[@id='supplierEmailId']")
    page.fill("xpath=//input[@id='supplierEmailId']", email_id)
    page.click("xpath=//input[@id='organisationName']")
    page.fill("xpath=//input[@id='organisationName']", 'ABCD')
    page.select_option("#country", "India")
    page.click("xpath=//input[@id='addressLine1']")
    page.fill("xpath=//input[@id='addressLine1']", 'ABC 1st')
    page.click("xpath=//input[@id='addressLine2']")
    page.fill("xpath=//input[@id='addressLine2']", 'EFGH')
    page.click("xpath=//input[@id='city']")
    page.fill("xpath=//input[@id='city']", 'Chennai')
    page.select_option("#state", "Tamil Nadu")
    page.click("xpath=//input[@id='zipcode']")
    page.fill("xpath=//input[@id='zipcode']", '600001')
    page.click("xpath=//button[contains(text(),'Proceed')]")

    file_path = "/Users/r0n01gu/Documents/sample-pdf.pdf"
    if os.path.exists(file_path):
        page.set_input_files("//label[@for='fileSelect']", file_path)
        print("File uploaded successfully")
    else:
        print("Sample PDF not found, skipping file upload")
    
    page.click("xpath=//input[@id='disablePartnerId']")
    page.click("xpath=//button[contains(text(),'Proceed')]")

    page.wait_for_load_state("load", timeout=60000)
    privacy_request_element = page.wait_for_selector("//*[@id='__next']/div[1]/section/div[1]/p/b[1]", timeout=60000)
    privacy_request_id = privacy_request_element.text_content()
    privacy_request_id = privacy_request_id.replace("#", "").replace(" ", "").strip()
    print(f"Privacy Request ID captured: {privacy_request_id}")
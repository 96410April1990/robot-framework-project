"""
OTP and CAPTCHA Handler for Playwright
Provides utilities for automating OTP entry and CAPTCHA solving
"""

import re
import time
import json
import requests
from typing import Optional, List
from playwright.sync_api import Page, expect


class OTPHandler:
    """Handle One-Time Password (OTP) automation"""
    
    @staticmethod
    def enter_otp_from_clipboard(page: Page, otp_input_selector: str, timeout: int = 10):
        """
        Wait for user to paste OTP and auto-fill the field
        Useful for manual copy-paste workflows
        """
        print(f"⏳ Waiting for OTP to be pasted (Ctrl+V)...")
        page.wait_for_timeout(timeout * 1000)
        
        # Try to fill the OTP field
        otp_field = page.locator(otp_input_selector)
        if otp_field.is_visible():
            otp_field.focus()
            page.keyboard.press("Control+V")
            time.sleep(0.5)
            return True
        return False
    
    @staticmethod
    def enter_otp_from_email(otp_input_selector: str, email: str, 
                            email_provider_api_key: str, timeout: int = 30) -> bool:
        """
        Extract OTP from email using MailSlurp or similar service
        
        Args:
            otp_input_selector: CSS selector for OTP input field
            email: Email address to check for OTP
            email_provider_api_key: API key for email service (MailSlurp, etc.)
            timeout: Time in seconds to wait for email
        
        Example:
            otp = OTPHandler.enter_otp_from_email(
                page,
                "input[name='otp']",
                "test@mailslurp.com",
                "your_mailslurp_api_key"
            )
        """
        print(f"📧 Fetching OTP from {email}...")
        
        try:
            # Using MailSlurp API as example
            headers = {
                "x-api-key": email_provider_api_key
            }
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                response = requests.get(
                    f"https://api.mailslurp.com/waitForLatestEmail?inboxId={email}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    email_data = response.json()
                    body = email_data.get("body", "")
                    
                    # Extract OTP using regex (adjust pattern as needed)
                    otp_match = re.search(r'\b(\d{4,6})\b', body)
                    if otp_match:
                        otp = otp_match.group(1)
                        print(f"✅ OTP found: {otp}")
                        return otp
                
                time.sleep(2)  # Retry every 2 seconds
            
            print("❌ OTP not received in time")
            return None
            
        except Exception as e:
            print(f"❌ Error fetching OTP: {e}")
            return None
    
    @staticmethod
    def enter_otp_from_twilio(page: Page, otp_input_selector: str, 
                             phone_number: str, account_sid: str, 
                             auth_token: str, timeout: int = 30) -> bool:
        """
        Extract OTP from SMS using Twilio API
        
        Args:
            page: Playwright Page object
            otp_input_selector: CSS selector for OTP input
            phone_number: Phone number to monitor (format: +1234567890)
            account_sid: Twilio Account SID
            auth_token: Twilio Auth Token
            timeout: Wait time in seconds
        
        Example:
            success = OTPHandler.enter_otp_from_twilio(
                page,
                "input#otp",
                "+1234567890",
                "your_account_sid",
                "your_auth_token"
            )
        """
        print(f"📱 Fetching OTP from SMS to {phone_number}...")
        
        try:
            from twilio.rest import Client
            client = Client(account_sid, auth_token)
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Get recent messages
                messages = client.messages.list(limit=5)
                
                for message in messages:
                    # Check if message is recent and contains OTP
                    otp_match = re.search(r'\b(\d{4,6})\b', message.body)
                    if otp_match and phone_number in str(message.from_):
                        otp = otp_match.group(1)
                        print(f"✅ OTP received via SMS: {otp}")
                        
                        # Fill the OTP field
                        otp_field = page.locator(otp_input_selector)
                        otp_field.fill(otp)
                        time.sleep(0.5)
                        return True
                
                time.sleep(2)
            
            print("❌ OTP SMS not received in time")
            return False
            
        except ImportError:
            print("⚠️  Install twilio: pip install twilio")
            return False
        except Exception as e:
            print(f"❌ Error fetching OTP from SMS: {e}")
            return False
    
    @staticmethod
    def enter_otp_manually(page: Page, otp_input_selector: str, timeout: int = 60) -> bool:
        """
        Prompt user to enter OTP manually with visual indicator
        
        Args:
            page: Playwright Page object
            otp_input_selector: CSS selector for OTP input
            timeout: Wait time in seconds
        
        Useful when: Testing in CI/CD or when automated OTP is not available
        """
        print(f"⏱️  Please enter OTP in the browser window (timeout: {timeout}s)...")
        
        try:
            otp_field = page.locator(otp_input_selector)
            
            # Highlight the OTP field with JavaScript
            page.evaluate("""
                (selector) => {
                    const el = document.querySelector(selector);
                    if (el) {
                        el.style.border = '3px solid red';
                        el.style.boxShadow = '0 0 10px red';
                        el.focus();
                    }
                }
            """, otp_input_selector)
            
            # Wait for user to fill the field
            expect(otp_field).to_have_value(re.compile(r'\d+'), timeout=timeout * 1000)
            print("✅ OTP entered successfully")
            return True
            
        except Exception as e:
            print(f"❌ Timeout waiting for OTP input: {e}")
            return False


class CAPTCHAHandler:
    """Handle CAPTCHA solving in Playwright"""
    
    @staticmethod
    def solve_recaptcha_v2(page: Page, api_key_2captcha: str, timeout: int = 120) -> bool:
        """
        Solve reCAPTCHA v2 using 2Captcha service
        
        Args:
            page: Playwright Page object
            api_key_2captcha: 2Captcha API key
            timeout: Wait time in seconds
        
        How it works:
            1. Extracts sitekey from page
            2. Sends to 2Captcha service
            3. Polls for solution
            4. Injects solution into page
        """
        print("🤖 Solving reCAPTCHA v2...")
        
        try:
            # Get sitekey from page
            sitekey = page.evaluate("""
                () => {
                    const iframe = document.querySelector('[src*="recaptcha"]');
                    if (iframe && iframe.src) {
                        const match = iframe.src.match(/k=([a-zA-Z0-9_-]+)/);
                        return match ? match[1] : null;
                    }
                    
                    // Alternative: check data attributes
                    const recaptchaElement = document.querySelector('[data-sitekey]');
                    return recaptchaElement ? recaptchaElement.getAttribute('data-sitekey') : null;
                }
            """)
            
            if not sitekey:
                print("❌ Could not find reCAPTCHA sitekey")
                return False
            
            print(f"🔑 Found sitekey: {sitekey[:20]}...")
            
            # Send to 2Captcha
            captcha_url = page.url
            submit_response = requests.post(
                "http://2captcha.com/api/upload",
                data={
                    'key': api_key_2captcha,
                    'method': 'userrecaptcha',
                    'googlekey': sitekey,
                    'pageurl': captcha_url,
                }
            )
            
            captcha_id = submit_response.text.split('=')[1]
            print(f"📤 CAPTCHA submitted, ID: {captcha_id}")
            
            # Poll for result
            start_time = time.time()
            while time.time() - start_time < timeout:
                result_response = requests.get(
                    f"http://2captcha.com/api/res?key={api_key_2captcha}&action=get&id={captcha_id}"
                )
                
                if "OK" in result_response.text:
                    captcha_solution = result_response.text.split('|')[1]
                    print(f"✅ CAPTCHA solved!")
                    
                    # Inject solution
                    page.evaluate(f"""
                        (token) => {{
                            document.getElementById('g-recaptcha-response').innerHTML = token;
                            document.querySelector('[name="g-recaptcha-response"]').value = token;
                            
                            // Trigger callback if exists
                            if (window.___grecaptcha_cfg) {{
                                Object.entries(window.___grecaptcha_cfg.clients).forEach(([key, client]) => {{
                                    if (client.callback) {{
                                        client.callback(token);
                                    }}
                                }});
                            }}
                        }}
                    """, captcha_solution)
                    
                    return True
                
                time.sleep(3)
            
            print("❌ CAPTCHA solving timed out")
            return False
            
        except Exception as e:
            print(f"❌ Error solving reCAPTCHA: {e}")
            return False
    
    @staticmethod
    def solve_hcaptcha(page: Page, api_key_2captcha: str, timeout: int = 120) -> bool:
        """
        Solve hCaptcha using 2Captcha service
        Similar to reCAPTCHA but with hCaptcha-specific logic
        """
        print("🤖 Solving hCaptcha...")
        
        try:
            # Get sitekey from hCaptcha
            sitekey = page.evaluate("""
                () => {
                    const element = document.querySelector('[data-sitekey]');
                    return element ? element.getAttribute('data-sitekey') : null;
                }
            """)
            
            if not sitekey:
                print("❌ Could not find hCaptcha sitekey")
                return False
            
            captcha_url = page.url
            
            # Submit to 2Captcha
            submit_response = requests.post(
                "http://2captcha.com/api/upload",
                data={
                    'key': api_key_2captcha,
                    'method': 'hcaptcha',
                    'sitekey': sitekey,
                    'pageurl': captcha_url,
                }
            )
            
            captcha_id = submit_response.text.split('=')[1]
            
            # Poll for result
            start_time = time.time()
            while time.time() - start_time < timeout:
                result_response = requests.get(
                    f"http://2captcha.com/api/res?key={api_key_2captcha}&action=get&id={captcha_id}"
                )
                
                if "OK" in result_response.text:
                    captcha_solution = result_response.text.split('|')[1]
                    print(f"✅ hCaptcha solved!")
                    
                    # Inject solution
                    page.evaluate(f"""
                        (token) => {{
                            document.querySelector('[name="h-captcha-response"]').value = token;
                            document.querySelector('[name="g-recaptcha-response"]').value = token;
                        }}
                    """, captcha_solution)
                    
                    return True
                
                time.sleep(3)
            
            print("❌ hCaptcha solving timed out")
            return False
            
        except Exception as e:
            print(f"❌ Error solving hCaptcha: {e}")
            return False
    
    @staticmethod
    def bypass_captcha_manually(page: Page, timeout: int = 60) -> bool:
        """
        Wait for user to manually solve CAPTCHA
        Visual indicator shows user where to solve
        """
        print(f"⏱️  Please solve CAPTCHA in browser (timeout: {timeout}s)...")
        
        try:
            # Highlight CAPTCHA elements
            page.evaluate("""
                () => {
                    const captchaElements = document.querySelectorAll(
                        '[class*="captcha"], [id*="captcha"], iframe[src*="recaptcha"], iframe[src*="hcaptcha"]'
                    );
                    captchaElements.forEach(el => {
                        el.style.border = '3px solid red';
                        el.style.boxShadow = '0 0 15px red';
                    });
                }
            """)
            
            # Wait for CAPTCHA response field to be populated
            page.wait_for_function("""
                () => {
                    const g_response = document.querySelector('[name="g-recaptcha-response"]');
                    const h_response = document.querySelector('[name="h-captcha-response"]');
                    return (g_response && g_response.value) || (h_response && h_response.value);
                }
            """, timeout=timeout * 1000)
            
            print("✅ CAPTCHA solved by user")
            return True
            
        except Exception as e:
            print(f"❌ Timeout waiting for CAPTCHA: {e}")
            return False
    
    @staticmethod
    def detect_captcha_type(page: Page) -> Optional[str]:
        """
        Detect which CAPTCHA type is on the page
        Returns: 'recaptcha_v2', 'recaptcha_v3', 'hcaptcha', 'cloudflare', or None
        """
        captcha_type = page.evaluate("""
            () => {
                // Check for reCAPTCHA v2/v3
                if (document.querySelector('[data-sitekey]')) {
                    return 'recaptcha';
                }
                
                // Check for hCaptcha
                if (document.querySelector('[data-sitekey][src*="hcaptcha"]')) {
                    return 'hcaptcha';
                }
                
                // Check for Cloudflare
                if (document.querySelector('[name="cf_turnstile_response"]')) {
                    return 'cloudflare_turnstile';
                }
                
                // Check for image CAPTCHA
                if (document.querySelector('[alt*="captcha" i], img[src*="captcha" i]')) {
                    return 'image_captcha';
                }
                
                return null;
            }
        """)
        
        if captcha_type:
            print(f"🔍 Detected CAPTCHA type: {captcha_type}")
        else:
            print("🔍 No CAPTCHA detected")
        
        return captcha_type


# ============= EXAMPLE USAGE =============

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Example 1: Manual OTP entry
        # page.goto("https://login.example.com")
        # OTPHandler.enter_otp_manually(page, "input[name='otp']", timeout=30)
        
        # Example 2: CAPTCHA detection
        # page.goto("https://example-with-captcha.com")
        # captcha_type = CAPTCHAHandler.detect_captcha_type(page)
        
        # Example 3: Solve reCAPTCHA v2
        # success = CAPTCHAHandler.solve_recaptcha_v2(
        #     page, 
        #     api_key_2captcha="your_2captcha_api_key"
        # )
        
        browser.close()

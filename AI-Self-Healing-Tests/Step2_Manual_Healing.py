#!/usr/bin/env python3
"""
Step 2: Manual Healing (Basic Solution)
======================================

This step shows how to add FALLBACK STRATEGIES to make tests more resilient.
When the primary locator fails, we try alternative ways to find the element.

🎯 Learning Goals:
- Understand fallback strategies
- See how multiple locators work together  
- Learn the difference between brittle and resilient tests

📚 Concepts Covered:
- Multiple locator strategies (ID → Name → Class → Text)
- Try-except pattern for fallbacks
- Manual healing logic
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os

class ManualHealingTest:
    """A test with manual fallback strategies for element location"""
    
    def __init__(self):
        self.driver = None
        self.healing_attempts = []
        self.test_results = []
    
    def setup_browser(self):
        """Set up the web browser for testing"""
        print("🚀 Setting up browser...")
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        print("✅ Browser ready!")
    
    def teardown_browser(self):
        """Clean up and close the browser"""
        if self.driver:
            print("🧹 Closing browser...")
            self.driver.quit()
    
    def find_element_with_healing(self, element_name, strategies):
        """
        Try multiple strategies to find an element
        
        Args:
            element_name: Human-readable name for the element
            strategies: List of (locator_type, locator_value, strategy_name) tuples
        
        Returns:
            WebElement if found, None if all strategies fail
        """
        print(f"🔍 Searching for '{element_name}' with healing...")
        
        for i, (locator_type, locator_value, strategy_name) in enumerate(strategies, 1):
            try:
                print(f"   Strategy {i}: {strategy_name} -> {locator_value}")
                element = self.driver.find_element(locator_type, locator_value)
                
                # Record successful healing
                healing_info = {
                    'element_name': element_name,
                    'successful_strategy': strategy_name,
                    'successful_locator': locator_value,
                    'attempts_needed': i
                }
                self.healing_attempts.append(healing_info)
                
                if i == 1:
                    print(f"   ✅ Found immediately using primary strategy!")
                else:
                    print(f"   🎯 HEALING SUCCESS! Found using fallback strategy {i}")
                    print(f"   💡 Primary locator failed, but healing worked!")
                
                return element
                
            except NoSuchElementException:
                print(f"   ❌ Strategy {i} failed: Element not found")
                continue
        
        # All strategies failed
        print(f"   💥 All healing strategies failed for '{element_name}'")
        return None
    
    def fill_text_with_healing(self, element_name, text, strategies):
        """Fill text field with healing capabilities"""
        element = self.find_element_with_healing(element_name, strategies)
        if element:
            element.clear()
            element.send_keys(text)
            print(f"   📝 Text entered: {text}")
            return True
        else:
            print(f"   ❌ Could not fill '{element_name}' - no healing strategy worked")
            return False
    
    def select_dropdown_with_healing(self, element_name, value, strategies):
        """Select dropdown option with healing capabilities"""
        element = self.find_element_with_healing(element_name, strategies)
        if element:
            dropdown = Select(element)
            dropdown.select_by_value(value)
            print(f"   🔽 Option selected: {value}")
            return True
        else:
            print(f"   ❌ Could not select from '{element_name}' - no healing strategy worked")
            return False
    
    def click_with_healing(self, element_name, strategies):
        """Click element with healing capabilities"""
        element = self.find_element_with_healing(element_name, strategies)
        if element:
            element.click()
            print(f"   🖱️ Element clicked successfully")
            return True
        else:
            print(f"   ❌ Could not click '{element_name}' - no healing strategy worked")
            return False
    
    def test_with_manual_healing(self, page_type, file_name):
        """Test a page using manual healing strategies"""
        print(f"\n" + "="*60)
        print(f"🧪 TESTING: {page_type} Page with Manual Healing")
        print("="*60)
        
        try:
            # Load the page
            current_dir = os.path.dirname(os.path.abspath(__file__))
            test_page_path = os.path.join(current_dir, file_name)
            file_url = f"file://{test_page_path}"
            
            print(f"📂 Loading page: {file_url}")
            self.driver.get(file_url)
            time.sleep(2)  # Let page load
            
            # Step 1: Fill email field with multiple strategies
            print("\n👤 Step 1: Email Field")
            email_strategies = [
                (By.ID, "email", "Primary ID"),
                (By.ID, "user-email", "Alternative ID"), 
                (By.NAME, "email", "Name attribute"),
                (By.NAME, "userEmail", "Alternative name"),
                (By.CSS_SELECTOR, "input[type='email']", "Email input type"),
                (By.XPATH, "//input[contains(@placeholder, 'email')]", "Placeholder text")
            ]
            
            email_success = self.fill_text_with_healing(
                "email field", "test@example.com", email_strategies
            )
            
            # Step 2: Fill password field with multiple strategies  
            print("\n🔒 Step 2: Password Field")
            password_strategies = [
                (By.ID, "password", "Primary ID"),
                (By.ID, "user-password", "Alternative ID"),
                (By.NAME, "password", "Name attribute"), 
                (By.NAME, "userPassword", "Alternative name"),
                (By.CSS_SELECTOR, "input[type='password']", "Password input type"),
                (By.XPATH, "//input[contains(@placeholder, 'password')]", "Placeholder text")
            ]
            
            password_success = self.fill_text_with_healing(
                "password field", "password123", password_strategies
            )
            
            # Step 3: Select country with multiple strategies
            print("\n🌍 Step 3: Country Dropdown")
            country_strategies = [
                (By.ID, "country", "Primary ID"),
                (By.ID, "user-country", "Alternative ID"),
                (By.NAME, "country", "Name attribute"),
                (By.NAME, "userCountry", "Alternative name"),
                (By.TAG_NAME, "select", "Generic select tag")
            ]
            
            country_success = self.select_dropdown_with_healing(
                "country dropdown", "us", country_strategies
            )
            
            # Step 4: Click submit button with multiple strategies
            print("\n🎯 Step 4: Submit Button")
            submit_strategies = [
                (By.ID, "submit-btn", "Primary ID"),
                (By.ID, "login-submit-button", "Alternative ID"),
                (By.CLASS_NAME, "submit-btn", "Primary class"),
                (By.CLASS_NAME, "login-button", "Alternative class"),
                (By.CSS_SELECTOR, "button[type='submit']", "Submit button type"),
                (By.XPATH, "//button[contains(text(), 'Login')]", "Button text"),
                (By.CSS_SELECTOR, "[data-testid='login-btn']", "Test ID attribute")
            ]
            
            submit_success = self.click_with_healing("submit button", submit_strategies)
            
            # Step 5: Wait for success message
            print("\n⏳ Step 5: Success Message")
            success_strategies = [
                (By.ID, "success-message", "Primary ID"),
                (By.ID, "login-success-notification", "Alternative ID"),
                (By.CLASS_NAME, "message", "Primary class"),
                (By.CLASS_NAME, "notification", "Alternative class"),
                (By.XPATH, "//div[contains(text(), 'Success')]", "Success text")
            ]
            
            success_element = self.find_element_with_healing("success message", success_strategies)
            
            if success_element and email_success and password_success and country_success and submit_success:
                # Wait for the message to be visible
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of(success_element)
                )
                print("   ✅ Success message appeared!")
                
                self.test_results.append({
                    'page_type': page_type,
                    'result': 'SUCCESS',
                    'healing_used': len([h for h in self.healing_attempts if h['attempts_needed'] > 1]) > 0
                })
                
                print(f"\n🎉 TEST RESULT: SUCCESS!")
                print(f"   All steps completed using manual healing strategies")
            else:
                raise Exception("One or more steps failed despite healing attempts")
                
        except Exception as e:
            print(f"\n❌ TEST RESULT: FAILED!")
            print(f"   Error: {str(e)}")
            self.test_results.append({
                'page_type': page_type,
                'result': 'FAILED',
                'error': str(e)
            })
        
        time.sleep(3)  # Pause to see the result
    
    def show_healing_analysis(self):
        """Show detailed analysis of healing attempts"""
        print("\n" + "="*60)
        print("📊 HEALING ANALYSIS")
        print("="*60)
        
        if not self.healing_attempts:
            print("🤔 No healing attempts needed - all primary locators worked!")
            return
        
        print(f"\n🔧 Healing Attempts: {len(self.healing_attempts)}")
        
        for attempt in self.healing_attempts:
            if attempt['attempts_needed'] > 1:
                print(f"\n🎯 HEALING SUCCESS:")
                print(f"   Element: {attempt['element_name']}")
                print(f"   Strategy: {attempt['successful_strategy']}")
                print(f"   Locator: {attempt['successful_locator']}")
                print(f"   Attempts needed: {attempt['attempts_needed']}")
            else:
                print(f"✅ No healing needed for: {attempt['element_name']}")
    
    def show_learning_summary(self):
        """Show what we learned from this step"""
        print("\n" + "="*60)
        print("📚 WHAT WE LEARNED - STEP 2")
        print("="*60)
        
        print("\n🎯 Manual Healing Concept:")
        print("   • Define multiple ways to find the same element")
        print("   • Try primary locator first, fall back to alternatives")
        print("   • Each element has several 'backup' strategies")
        print("   • Tests become resilient instead of brittle")
        
        print(f"\n📊 Test Results Summary:")
        for result in self.test_results:
            status_emoji = "✅" if result['result'] == 'SUCCESS' else "❌"
            healing_emoji = "🎯" if result.get('healing_used', False) else "➡️"
            print(f"   {status_emoji} {result['page_type']}: {result['result']} {healing_emoji}")
        
        print(f"\n💡 Benefits Seen:")
        healing_count = len([h for h in self.healing_attempts if h['attempts_needed'] > 1])
        if healing_count > 0:
            print(f"   • {healing_count} elements needed healing - but tests still passed!")
            print(f"   • Without healing: {healing_count} test failures")
            print(f"   • With healing: 0 test failures")
            print(f"   • Time saved: ~{healing_count * 30} minutes of manual fixes")
        else:
            print("   • All primary locators worked - healing ready as backup")
            print("   • Tests are now resilient to future changes")
        
        print(f"\n🤔 Limitations of Manual Healing:")
        print("   • Must manually define all possible locator strategies")
        print("   • Cannot adapt to completely new page layouts")
        print("   • No learning - same fallbacks every time")
        print("   • Still requires human knowledge of element attributes")
        
        print(f"\n🚀 Next Step:")
        print("   Run 'Step3_Smart_Healing.py' to see intelligent healing!")
        print("   We'll make the system smarter at generating fallbacks automatically.")

def main():
    """Run the manual healing demonstration"""
    print("🎓 STEP 2: Manual Healing with Fallback Strategies")
    print("="*60)
    print("This demonstrates how multiple locator strategies make tests resilient.")
    print("We'll test both pages and see how healing prevents failures.")
    
    # Create and run the test
    test = ManualHealingTest()
    
    try:
        test.setup_browser()
        
        # Test 1: Original page
        test.test_with_manual_healing("Original", "test_page.html")
        
        # Test 2: Changed page (should now work with healing!)
        test.test_with_manual_healing("Changed", "test_page_changed.html")
        
        # Show healing analysis
        test.show_healing_analysis()
        
        # Show what we learned
        test.show_learning_summary()
        
    finally:
        test.teardown_browser()
    
    print(f"\n🎯 Ready for Step 3? Run: python3 Step3_Smart_Healing.py")

if __name__ == "__main__":
    main()
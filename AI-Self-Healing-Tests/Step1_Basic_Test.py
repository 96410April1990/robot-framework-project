#!/usr/bin/env python3
"""
Step 1: Basic Test (The Problem)
===============================

This is a NORMAL test that works with the original web page but BREAKS
when developers change element IDs. This demonstrates the problem that
self-healing tests solve.

🎯 Learning Goals:
- Understand how normal tests work
- See what happens when locators break
- Understand why we need self-healing

📚 Concepts Covered:
- Web element locators (ID, name, class)
- Basic Selenium operations
- Why tests become "brittle"
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os

class BasicTest:
    """A normal, brittle test that breaks when element IDs change"""
    
    def __init__(self):
        self.driver = None
        self.test_results = []
    
    def setup_browser(self):
        """Set up the web browser for testing"""
        print("🚀 Setting up browser...")
        self.driver = webdriver.Chrome()  # Make sure you have chromedriver installed
        self.driver.maximize_window()
        print("✅ Browser ready!")
    
    def teardown_browser(self):
        """Clean up and close the browser"""
        if self.driver:
            print("🧹 Closing browser...")
            self.driver.quit()
    
    def test_original_page(self):
        """Test with the original page (should work)"""
        print("\n" + "="*60)
        print("🧪 TEST 1: Original Page (Should Work)")
        print("="*60)
        
        try:
            # Get the path to our test HTML file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            test_page_path = os.path.join(current_dir, "test_page.html")
            file_url = f"file://{test_page_path}"
            
            print(f"📂 Loading page: {file_url}")
            self.driver.get(file_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            
            print("👤 Step 1: Filling email field...")
            email_field = self.driver.find_element(By.ID, "email")
            email_field.send_keys("test@example.com")
            print("   ✅ Email entered: test@example.com")
            
            print("🔒 Step 2: Filling password field...")
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys("password123")
            print("   ✅ Password entered: ********")
            
            print("🌍 Step 3: Selecting country...")
            country_dropdown = Select(self.driver.find_element(By.ID, "country"))
            country_dropdown.select_by_value("us")
            print("   ✅ Country selected: United States")
            
            print("🎯 Step 4: Clicking submit button...")
            submit_button = self.driver.find_element(By.ID, "submit-btn")
            submit_button.click()
            print("   ✅ Submit button clicked")
            
            # Wait for success message
            print("⏳ Step 5: Waiting for success message...")
            success_message = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, "success-message"))
            )
            print("   ✅ Success message appeared!")
            
            print("\n🎉 TEST RESULT: SUCCESS!")
            print("   All elements found using their original IDs")
            
            self.test_results.append({
                'test': 'Original Page', 
                'result': 'SUCCESS',
                'reason': 'All original locators worked'
            })
            
        except Exception as e:
            print(f"\n❌ TEST RESULT: FAILED!")
            print(f"   Error: {str(e)}")
            self.test_results.append({
                'test': 'Original Page', 
                'result': 'FAILED', 
                'reason': str(e)
            })
        
        time.sleep(3)  # Pause to see the result
    
    def test_changed_page(self):
        """Test with the changed page (will break)"""
        print("\n" + "="*60)
        print("🧪 TEST 2: Changed Page (Will Break)")
        print("="*60)
        
        try:
            # Load the changed version of the page
            current_dir = os.path.dirname(os.path.abspath(__file__))
            test_page_path = os.path.join(current_dir, "test_page_changed.html")
            file_url = f"file://{test_page_path}"
            
            print(f"📂 Loading changed page: {file_url}")
            self.driver.get(file_url)
            
            # This will fail because the IDs have changed!
            print("👤 Step 1: Trying to fill email field with OLD locator...")
            print("   🔍 Looking for element with ID 'email'...")
            
            try:
                email_field = self.driver.find_element(By.ID, "email")
                email_field.send_keys("test@example.com")
                print("   ✅ Somehow this worked? (Unexpected)")
            except NoSuchElementException:
                print("   ❌ FAILED! Element with ID 'email' not found!")
                print("   💡 The developer changed it to ID 'user-email'")
                raise Exception("Element locator 'email' no longer exists")
            
        except Exception as e:
            print(f"\n💥 TEST RESULT: FAILED (As Expected)!")
            print(f"   Error: {str(e)}")
            print("\n🤔 What Happened?")
            print("   • Developer changed element IDs")
            print("   • Our test still uses OLD locators") 
            print("   • Test breaks even though page functionality is the same")
            print("   • Manual fix needed: Update all locators in test code")
            
            self.test_results.append({
                'test': 'Changed Page', 
                'result': 'FAILED (Expected)', 
                'reason': 'Element locators changed, test not updated'
            })
    
    def show_learning_summary(self):
        """Show what we learned from this step"""
        print("\n" + "="*60)
        print("📚 WHAT WE LEARNED - STEP 1")
        print("="*60)
        
        print("\n🎯 The Problem:")
        print("   • Tests break when developers change element IDs/classes")
        print("   • Same functionality, different locators = test failure")
        print("   • Manual effort required to fix each broken test")
        print("   • Wastes time and delays releases")
        
        print("\n📊 Test Results Summary:")
        for result in self.test_results:
            status_emoji = "✅" if "SUCCESS" in result['result'] else "❌"
            print(f"   {status_emoji} {result['test']}: {result['result']}")
            print(f"      Reason: {result['reason']}")
        
        print("\n💡 Real-World Impact:")
        print("   • 30 minutes to fix each broken locator manually")
        print("   • Multiply by 100+ tests = 50+ hours of maintenance")
        print("   • Tests become 'brittle' and unreliable")
        print("   • Teams start skipping automated tests")
        
        print("\n🚀 Next Step:")
        print("   Run 'Step2_Manual_Healing.py' to see how we can fix this!")
        print("   We'll add fallback strategies that work automatically.")

def main():
    """Run the basic test demonstration"""
    print("🎓 STEP 1: Understanding the Problem")
    print("="*60)
    print("This demonstrates why normal tests are 'brittle' and break easily.")
    print("We'll test the same functionality on two versions of a web page.")
    
    # Create and run the test
    test = BasicTest()
    
    try:
        test.setup_browser()
        
        # Test 1: Original page (should work)
        test.test_original_page()
        
        # Test 2: Changed page (will fail)
        test.test_changed_page()
        
        # Show what we learned
        test.show_learning_summary()
        
    finally:
        test.teardown_browser()
    
    print(f"\n🎯 Ready for Step 2? Run: python3 Step2_Manual_Healing.py")

if __name__ == "__main__":
    main()
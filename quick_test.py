#!/usr/bin/env python3
"""
Quick Test Script for IRCTC Bot
Tests only the essential components without full browser initialization
"""

import sys
import importlib

def test_basic_imports():
    """Test if core packages can be imported"""
    print("🔍 Testing basic imports...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        print("✅ Selenium imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config_validation():
    """Test configuration"""
    print("\n🔍 Testing configuration...")
    
    try:
        import config
        
        # Check if credentials are updated
        if config.IRCTC_USERNAME == "your_username" or config.IRCTC_PASSWORD == "your_password":
            print("⚠️  Warning: Please update IRCTC_USERNAME and IRCTC_PASSWORD in config.py")
            
        # Check journey details
        print(f"✅ From: {config.FROM_STATION} To: {config.TO_STATION}")
        print(f"✅ Date: {config.JOURNEY_DATE} Class: {config.JOURNEY_CLASS}")
        
        # Check passenger details
        if config.PASSENGERS and len(config.PASSENGERS) > 0:
            print(f"✅ {len(config.PASSENGERS)} passenger(s) configured")
        else:
            print("❌ No passengers configured")
            return False
            
        print("✅ Configuration looks good")
        return True
        
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_bot_initialization():
    """Test if the bot class can be imported and basic methods exist"""
    print("\n🔍 Testing bot class...")
    
    try:
        from irctc_bot import IRCTCBot
        
        # Check if key methods exist
        bot_methods = ['login', 'search_trains', 'select_train_and_book', 'fill_passenger_details', 'make_payment']
        
        for method in bot_methods:
            if hasattr(IRCTCBot, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        print("✅ Bot class structure is valid")
        return True
        
    except Exception as e:
        print(f"❌ Bot initialization error: {e}")
        return False

def test_date_validation():
    """Test if the journey date is valid"""
    print("\n🔍 Testing journey date...")
    
    try:
        import config
        from datetime import datetime
        
        # Parse the date
        journey_date = datetime.strptime(config.JOURNEY_DATE, "%d/%m/%Y")
        current_date = datetime.now()
        
        if journey_date < current_date:
            print("⚠️  Warning: Journey date is in the past")
        elif journey_date > current_date:
            days_diff = (journey_date - current_date).days
            if days_diff > 120:
                print("⚠️  Warning: Journey date is more than 120 days in the future (IRCTC booking limit)")
            else:
                print(f"✅ Journey date is valid ({days_diff} days from now)")
        
        return True
        
    except ValueError as e:
        print(f"❌ Invalid date format: {e}")
        print("Expected format: DD/MM/YYYY")
        return False
    except Exception as e:
        print(f"❌ Date validation error: {e}")
        return False

def main():
    """Run quick tests"""
    print("🚂 IRCTC Bot Quick Test")
    print("=" * 40)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Configuration", test_config_validation),
        ("Bot Class", test_bot_initialization),
        ("Date Validation", test_date_validation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Quick Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All quick tests passed!")
        print("\n✅ Your bot is ready for testing!")
        print("\nNext steps:")
        print("1. Update your IRCTC credentials in config.py if not done")
        print("2. Test with a dry run: python main.py")
        print("3. The bot will pause for manual captcha solving")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    print("\n💡 Tips for testing:")
    print("- Start with a test run during non-peak hours")
    print("- Have your payment details ready")
    print("- Be prepared to solve captcha manually")
    print("- Keep backup booking method ready")

if __name__ == "__main__":
    main()


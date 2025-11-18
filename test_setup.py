#!/usr/bin/env python3
"""
Test Setup Script
Verifies that all dependencies are installed and the bot can initialize properly
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'selenium',
        'webdriver_manager',
        'requests',
        'bs4'
    ]
    
    print("🔍 Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package} - {str(e)}")
            failed_imports.append(package)
    
    return len(failed_imports) == 0

def test_config():
    """Test if config file can be imported and has required fields"""
    print("\n🔍 Testing configuration...")
    
    try:
        import config
        print("✅ config.py imported successfully")
        
        required_fields = [
            'IRCTC_USERNAME', 'IRCTC_PASSWORD', 'FROM_STATION', 
            'TO_STATION', 'JOURNEY_DATE', 'JOURNEY_CLASS', 'PASSENGERS'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not hasattr(config, field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing required fields: {', '.join(missing_fields)}")
            return False
        else:
            print("✅ All required configuration fields present")
            return True
            
    except ImportError as e:
        print(f"❌ Failed to import config: {str(e)}")
        return False

def test_driver_setup():
    """Test if Chrome driver can be initialized"""
    print("\n🔍 Testing Chrome driver setup...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get("https://www.google.com")
        
        if "Google" in driver.title:
            print("✅ Chrome driver initialized successfully")
            driver.quit()
            return True
        else:
            print("❌ Chrome driver failed to load Google")
            driver.quit()
            return False
            
    except Exception as e:
        print(f"❌ Chrome driver setup failed: {str(e)}")
        return False

def test_irctc_connectivity():
    """Test if IRCTC website is accessible"""
    print("\n🔍 Testing IRCTC website connectivity...")
    
    try:
        import requests
        
        response = requests.get("https://www.irctc.co.in", timeout=10)
        if response.status_code == 200:
            print("✅ IRCTC website is accessible")
            return True
        else:
            print(f"❌ IRCTC website returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to connect to IRCTC: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🤖 IRCTC Bot Setup Test")
    print("=" * 40)
    
    tests = [
        ("Package Imports", test_imports),
        ("Configuration", test_config),
        ("Chrome Driver", test_driver_setup),
        ("IRCTC Connectivity", test_irctc_connectivity)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            if test_func():
                passed_tests += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {str(e)}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed_tests}/{total_tests} passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Update config.py with your actual details")
        print("2. Run: python main.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues before running the bot.")
        
        if passed_tests < 2:
            print("\nTroubleshooting tips:")
            print("- Run: pip install -r requirements.txt")
            print("- Make sure Chrome browser is installed")
            print("- Check your internet connection")
    
    print("=" * 40)

if __name__ == "__main__":
    main()

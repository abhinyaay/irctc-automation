#!/usr/bin/env python3
"""
IRCTC Tatkal Booking Bot - Main Script
Run this script to start the automated booking process

IMPORTANT NOTES:
1. Update config.py with your credentials and journey details before running
2. Make sure you have Chrome browser installed
3. Manual captcha solving may be required during login
4. Payment process may require manual intervention for OTP/2FA

LEGAL DISCLAIMER:
This bot is for educational purposes only. Please ensure you comply with
IRCTC's terms of service and use this responsibly.
"""

import sys
import logging
from irctc_bot import IRCTCBot
import config

def validate_config():
    """Validate that all required configurations are set"""
    required_fields = [
        'IRCTC_USERNAME', 'IRCTC_PASSWORD', 'FROM_STATION', 'TO_STATION',
        'JOURNEY_DATE', 'JOURNEY_CLASS', 'PASSENGERS'
    ]
    
    missing_fields = []
    for field in required_fields:
        value = getattr(config, field, None)
        if not value or (isinstance(value, str) and value.startswith('your_')):
            missing_fields.append(field)
    
    if missing_fields:
        print("❌ Configuration Error: Please update the following fields in config.py:")
        for field in missing_fields:
            print(f"   - {field}")
        return False
    
    # Validate passenger details
    if not config.PASSENGERS or len(config.PASSENGERS) == 0:
        print("❌ Configuration Error: Please add at least one passenger in config.py")
        return False
    
    for i, passenger in enumerate(config.PASSENGERS):
        required_passenger_fields = ['name', 'age', 'gender', 'berth_preference', 'id_card_type', 'id_card_number']
        for field in required_passenger_fields:
            if field not in passenger or not passenger[field]:
                print(f"❌ Configuration Error: Missing {field} for passenger {i+1}")
                return False
    
    # Validate payment method
    if config.PAYMENT_METHOD == "UPI" and not config.UPI_ID:
        print("❌ Configuration Error: UPI_ID is required when using UPI payment")
        return False
    
    return True

def print_journey_summary():
    """Print a summary of the booking details"""
    print("\n" + "="*60)
    print("🚂 IRCTC TATKAL BOOKING BOT")
    print("="*60)
    print(f"📍 From: {config.FROM_STATION}")
    print(f"📍 To: {config.TO_STATION}")
    print(f"📅 Date: {config.JOURNEY_DATE}")
    print(f"🎫 Class: {config.JOURNEY_CLASS}")
    print(f"👥 Passengers: {len(config.PASSENGERS)}")
    print(f"💳 Payment: {config.PAYMENT_METHOD}")
    if config.TRAIN_PREFERENCE:
        print(f"🚆 Preferred Train: {config.TRAIN_PREFERENCE}")
    print(f"⏰ Tatkal Time: {config.TATKAL_TIME}")
    print("="*60)

def main():
    """Main function to run the IRCTC booking bot"""
    print("🤖 IRCTC Tatkal Booking Bot Starting...")
    
    # Validate configuration
    if not validate_config():
        print("\n❌ Please fix the configuration errors and try again.")
        sys.exit(1)
    
    # Print journey summary
    print_journey_summary()
    
    # Confirm before starting
    confirm = input("\n⚠️  Are you sure you want to start the booking process? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ Booking cancelled by user.")
        sys.exit(0)
    
    # Legal disclaimer
    print("\n📋 LEGAL DISCLAIMER:")
    print("This bot is for educational purposes only.")
    print("Please ensure you comply with IRCTC's terms of service.")
    print("Use this bot responsibly and at your own risk.")
    
    disclaimer_confirm = input("\nDo you agree to the above terms? (y/N): ")
    if disclaimer_confirm.lower() != 'y':
        print("❌ Terms not accepted. Exiting...")
        sys.exit(0)
    
    try:
        # Initialize and run the bot
        bot = IRCTCBot()
        success = bot.run_booking_process()
        
        if success:
            print("\n✅ Booking process completed successfully!")
            print("Please check your IRCTC account and email for confirmation.")
        else:
            print("\n❌ Booking process failed. Please check the logs for details.")
            print("You may need to try again or book manually.")
    
    except KeyboardInterrupt:
        print("\n⚠️ Booking process interrupted by user.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")
        print("Please check the logs for more details.")
    
    print("\n🏁 Bot execution completed.")

if __name__ == "__main__":
    main()

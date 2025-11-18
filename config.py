"""
Configuration file for IRCTC automation bot
Fill in your details before running the bot
"""

# IRCTC Login Credentials
IRCTC_USERNAME = "Praveen1120"
IRCTC_PASSWORD = "Shashi@715"

# Journey Details
FROM_STATION = "AGC"  # Example: New Delhi
TO_STATION = "SC"     # Example: Mumbai Central
JOURNEY_DATE = "27/08/2024"  # DD/MM/YYYY format
JOURNEY_CLASS = "3A"   # Options: SL, 3A, 2A, 1A
TRAIN_PREFERENCE = "12951"  # Optional: Specific train number preference

# Passenger Details (List of passengers)
PASSENGERS = [
    {
        "name": "PASSENGER NAME",
        "age": 25,
        "gender": "M",  # M/F
        "berth_preference": "LB",  # UB/MB/LB/SU/SL
        "food_choice": "V",  # V for Veg, N for Non-Veg
        "id_card_type": "Aadhar",
        "id_card_number": "123456789012"
    }
]

# Payment Details
PAYMENT_METHOD = "UPI"  # UPI, DEBIT_CARD, CREDIT_CARD, NET_BANKING
UPI_ID = "your_upi_id@bank"

# Card Details (if using card payment)
CARD_NUMBER = ""
CARD_EXPIRY_MONTH = ""
CARD_EXPIRY_YEAR = ""
CARD_CVV = ""
CARD_HOLDER_NAME = ""

# Net Banking Details (if using net banking)
BANK_NAME = ""

# Automation Settings
HEADLESS_MODE = False  # Set to True to run browser in background
IMPLICIT_WAIT = 10     # Wait time in seconds
BOOKING_ATTEMPTS = 3   # Number of retry attempts
TATKAL_TIME = "10:00"  # Time to start booking (HH:MM format)

# Browser Settings
CHROME_DRIVER_PATH = None  # Leave None to auto-download driver

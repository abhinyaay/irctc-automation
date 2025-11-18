# IRCTC Tatkal Booking Bot 🚂

An automated Python bot for booking Tatkal tickets on IRCTC using Selenium WebDriver.

## About this project

This project automates the repetitive steps involved in booking Tatkal tickets on the IRCTC website.  
It is designed to help you pre‑configure journey, passenger, and payment details so that at Tatkal opening time the bot can execute the flow quickly and consistently while still keeping you in control for captcha and OTP steps.

## Why I built this

Tatkal booking windows are extremely competitive and even small delays in filling forms can lead to a failed booking.  
This bot was built:

- To **reduce manual typing and navigation time** during the Tatkal window
- To **standardize the booking flow** and avoid human errors in passenger or journey details
- To **experiment with Selenium automation** and browser‑based workflows in a real‑world scenario

Again, this is intended for **learning and personal experimentation**, not for abusing IRCTC systems.

## Tech stack & language

- **Language**: Python (3.7+)
- **Automation framework**: Selenium WebDriver
- **Browser**: Google Chrome
- **OS support**: Any OS that can run Python, Chrome, and ChromeDriver (tested primarily on desktop environments)

## ⚠️ Legal Disclaimer

This bot is created for **educational purposes only**. Please ensure you comply with IRCTC's terms of service and use this bot responsibly. The author is not responsible for any misuse or consequences arising from the use of this bot.

## Features

- ✅ Automated IRCTC login
- ✅ Train search between stations
- ✅ Tatkal ticket booking
- ✅ Passenger details auto-fill
- ✅ Multiple payment method support (UPI, Cards, Net Banking)
- ✅ Configurable retry attempts
- ✅ Timing controls for Tatkal booking windows
- ✅ Comprehensive logging

## Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- Valid IRCTC account
- Stable internet connection

## How to use

### 1. Clone the repository

```bash
git clone https://github.com/abhinyaay/irctc-automation.git
cd irctc-automation
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your details

Update `config.py` with your IRCTC login, journey details, passenger details, and payment preferences (see sections below).

### 5. Run the bot

```bash
python main.py
```

The bot will validate your configuration, wait for the Tatkal window (if configured), then guide you through captcha and payment steps.

## Installation (alternative quick steps)

1. Clone or download this repository
2. Install required dependencies with `pip install -r requirements.txt`

## Configuration

1. Open `config.py` and update the following details:

### Login Credentials
```python
IRCTC_USERNAME = "your_actual_username"
IRCTC_PASSWORD = "your_actual_password"
```

### Journey Details
```python
FROM_STATION = "NDLS"  # Station code (e.g., New Delhi)
TO_STATION = "BCT"     # Station code (e.g., Mumbai Central)
JOURNEY_DATE = "25/12/2024"  # DD/MM/YYYY format
JOURNEY_CLASS = "3A"   # SL, 3A, 2A, 1A
TRAIN_PREFERENCE = "12951"  # Optional: specific train number
```

### Passenger Details
```python
PASSENGERS = [
    {
        "name": "JOHN DOE",
        "age": 30,
        "gender": "M",  # M/F
        "berth_preference": "LB",  # UB/MB/LB/SU/SL
        "food_choice": "V",  # V for Veg, N for Non-Veg
        "id_card_type": "Aadhar",
        "id_card_number": "123456789012"
    }
    # Add more passengers as needed
]
```

### Payment Details
```python
PAYMENT_METHOD = "UPI"  # UPI, DEBIT_CARD, CREDIT_CARD, NET_BANKING
UPI_ID = "yourname@bank"  # For UPI payments
```

## Usage

1. Make sure all configurations are properly set in `config.py`

2. Run the bot:
```bash
python main.py
```

3. The bot will:
   - Validate your configuration
   - Show a summary of your booking details
   - Ask for confirmation
   - Wait for Tatkal time (if configured)
   - Attempt to book the ticket
   - Handle payment process

## Important Notes

### Manual Interventions Required

1. **Captcha Solving**: You'll need to manually solve the captcha during login
2. **Payment OTP**: Complete OTP verification for payment if required
3. **2FA Authentication**: Handle any two-factor authentication

### Tatkal Timing

- **AC Classes (1A, 2A, 3A)**: Booking opens at 10:00 AM
- **Non-AC Classes (SL, CC)**: Booking opens at 11:00 AM
- Set `TATKAL_TIME` in config.py accordingly

### Success Tips

1. **Fast Internet**: Ensure stable, high-speed internet connection
2. **System Time**: Keep your system clock synchronized
3. **Browser Updates**: Use the latest Chrome browser
4. **Practice**: Test the bot during non-peak hours first
5. **Backup Plan**: Keep manual booking as a backup option

## Troubleshooting

### Common Issues

1. **Driver Issues**:
   - Update Chrome browser
   - Clear browser cache
   - Try running with `HEADLESS_MODE = False`

2. **Login Problems**:
   - Verify credentials in config.py
   - Check if account is locked
   - Ensure captcha is solved correctly

3. **Booking Failures**:
   - Increase `BOOKING_ATTEMPTS` in config
   - Check if Tatkal quota is available
   - Verify passenger details format

4. **Payment Issues**:
   - Ensure payment details are correct
   - Have backup payment method ready
   - Complete OTP verification quickly

### Logs

Check the console output for detailed logs about the booking process. The bot provides comprehensive logging for debugging.

## File Structure

```
irctc-automation/
├── main.py              # Main script to run the bot
├── irctc_bot.py         # Core bot functionality
├── config.py            # Configuration file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Configuration Options

| Setting | Description | Example |
|---------|-------------|---------|
| `HEADLESS_MODE` | Run browser in background | `False` |
| `IMPLICIT_WAIT` | Wait time for elements | `10` |
| `BOOKING_ATTEMPTS` | Number of retry attempts | `3` |
| `TATKAL_TIME` | When to start booking | `"10:00"` |

## Supported Payment Methods

- **UPI**: Requires UPI ID
- **Debit Card**: Requires card details
- **Credit Card**: Requires card details  
- **Net Banking**: Requires bank selection

## Contributing

This project is for educational purposes. If you find bugs or have improvements, feel free to contribute responsibly.

## License

This project is provided as-is for educational purposes only. Use at your own risk.

---

**Remember**: Always respect IRCTC's terms of service and use automation tools responsibly. Happy booking! 🎫

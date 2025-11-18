"""
Station Code Lookup Utility
Helps find IRCTC station codes for your journey
"""

import requests
from bs4 import BeautifulSoup

def search_station_code(station_name):
    """Search for station code using station name"""
    try:
        # This is a simplified lookup - in reality, you might want to use IRCTC's official API
        # or maintain a local database of station codes
        
        common_stations = {
            "new delhi": "NDLS",
            "mumbai central": "BCT", 
            "mumbai": "CSTM",
            "bangalore": "SBC",
            "chennai": "MAS",
            "kolkata": "HWH",
            "hyderabad": "SC",
            "pune": "PUNE",
            "ahmedabad": "ADI",
            "jaipur": "JP",
            "lucknow": "LJN",
            "kanpur": "CNB",
            "nagpur": "NGP",
            "bhopal": "BPL",
            "indore": "INDB",
            "guwahati": "GHY",
            "patna": "PNBE",
            "ranchi": "RNC",
            "bhubaneswar": "BBS",
            "thiruvananthapuram": "TVC",
            "kochi": "ERS",
            "coimbatore": "CBE",
            "madurai": "MDU",
            "vijayawada": "BZA",
            "visakhapatnam": "VSKP",
            "jammu": "JAT",
            "dehradun": "DDN",
            "haridwar": "HW",
            "amritsar": "ASR",
            "chandigarh": "CDG",
            "jodhpur": "JU",
            "udaipur": "UDZ",
            "goa": "MAO",
            "mangalore": "MAJN",
            "mysore": "MYS"
        }
        
        station_lower = station_name.lower().strip()
        
        # Direct match
        if station_lower in common_stations:
            return common_stations[station_lower]
        
        # Partial match
        for station, code in common_stations.items():
            if station_lower in station or station in station_lower:
                return f"{code} (matched: {station})"
        
        return "Station not found in common stations list"
        
    except Exception as e:
        return f"Error searching for station: {str(e)}"

def print_common_stations():
    """Print a list of common station codes"""
    stations = {
        "NDLS": "New Delhi",
        "BCT": "Mumbai Central", 
        "CSTM": "Mumbai CST",
        "SBC": "Bangalore City",
        "MAS": "Chennai Central",
        "HWH": "Howrah (Kolkata)",
        "SC": "Secunderabad",
        "PUNE": "Pune Junction",
        "ADI": "Ahmedabad",
        "JP": "Jaipur",
        "LJN": "Lucknow Junction",
        "CNB": "Kanpur Central",
        "NGP": "Nagpur",
        "BPL": "Bhopal",
        "INDB": "Indore",
        "GHY": "Guwahati",
        "PNBE": "Patna Junction",
        "RNC": "Ranchi",
        "BBS": "Bhubaneswar",
        "TVC": "Thiruvananthapuram",
        "ERS": "Ernakulam (Kochi)",
        "CBE": "Coimbatore",
        "MDU": "Madurai",
        "BZA": "Vijayawada",
        "VSKP": "Visakhapatnam",
        "JAT": "Jammu Tawi",
        "DDN": "Dehradun",
        "HW": "Haridwar",
        "ASR": "Amritsar",
        "CDG": "Chandigarh",
        "JU": "Jodhpur",
        "UDZ": "Udaipur City",
        "MAO": "Madgaon (Goa)",
        "MAJN": "Mangalore Junction",
        "MYS": "Mysore"
    }
    
    print("\n" + "="*50)
    print("COMMON IRCTC STATION CODES")
    print("="*50)
    
    for code, name in sorted(stations.items()):
        print(f"{code:6} - {name}")
    
    print("="*50)

if __name__ == "__main__":
    print("🚂 IRCTC Station Code Lookup Tool")
    print_common_stations()
    
    while True:
        print("\nOptions:")
        print("1. Search for station code")
        print("2. Show all common stations")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            station_name = input("Enter station name: ").strip()
            if station_name:
                result = search_station_code(station_name)
                print(f"Result: {result}")
        elif choice == "2":
            print_common_stations()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

#!/usr/bin/env python3
"""SOTO FLIGHTS"""
"""My app will help you discover your next adventures with low flight fares."""
"""I invite you to a cup of coffee in the air."""

import time
from amadeus import Client, ResponseError
from colorama import Fore, Style, init
from rich.progress import Progress

# Initialize colorama
init(autoreset=True)

# Initialize the Amadeus client with your API credentials
amadeus = Client(
    client_id='YOUR_CLIENT_KEY',
    client_secret='YOUR_CLIENT_SECRET_KEY'
)

def search_airports_by_city(city_name):
    """Search for airports by city name."""
    try:
        response = amadeus.reference_data.locations.get(
            keyword=city_name,
            subType='AIRPORT'
        )
        airports = response.data
        if not airports:
            print("No airports found for the given city.")
            return None

        airport_codes = {}
        for airport in airports:
            code = airport['iataCode']
            name = airport['name']
            airport_codes[code] = name
            print(f"{code}: {name}")
        
        return airport_codes

    except ResponseError as error:
        print(f"An error occurred: {error}")
        return None

def search_cheapest_flights(origin, destination, departure_date, return_date=None):
    """Search for the cheapest flights and print the details with colored pricing."""
    try:
        # Create a progress bar and update it while waiting for the API call
        with Progress() as progress:
            task = progress.add_task("[cyan]Searching for flights...", total=100)
            for _ in range(10):
                time.sleep(1)  # Simulate delay for demonstration purposes
                progress.update(task, advance=10)

        if return_date:
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departure_date,
                returnDate=return_date,
                adults=1,
                currencyCode='USD'
            )
        else:
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departure_date,
                adults=1,
                currencyCode='USD'
            )
        
        flights = response.data
        if not flights:
            print("No flights found.")
            return

        sorted_flights = sorted(flights, key=lambda x: float(x['price']['total']))

        cheapest_flight = sorted_flights[0]
        price = float(cheapest_flight['price']['total'])
        
        if price <= 500:
            price_color = Fore.GREEN
        elif 500 < price < 1000:
            price_color = Fore.YELLOW
        else:
            price_color = Fore.RED

        print(f"Cheapest flight from {origin.upper()} to {destination.upper()}:")
        print(f"Price: {price_color}{cheapest_flight['price']['total']} {cheapest_flight['price']['currency']}{Style.RESET_ALL}")

        # Display flight details
        for itinerary in cheapest_flight['itineraries']:
            for segment in itinerary['segments']:
                print(f"  {segment['departure']['iataCode']} -> {segment['arrival']['iataCode']}")
                print(f"    Departure: {segment['departure']['at']}")
                print(f"    Arrival: {segment['arrival']['at']}")
            print()

        # Provide booking link
        flight_id = cheapest_flight['id']
        print("Booking Link: ", f"https://www.amadeus.com/book/{flight_id}")

    except ResponseError as error:
        print(f"An error occurred: {error}")

def get_airport_code(city_or_code_prompt):
    """Get an airport code by prompting for a city or airport code and listing options if needed."""
    input_value = input(city_or_code_prompt).strip().upper()
    
    if len(input_value) == 3:  # Assuming it's an airport code
        return input_value
    
    # Otherwise, treat it as a city name
    airports = search_airports_by_city(input_value)
    if not airports:
        return None
    
    airport_code = input("Enter the airport code from the list above: ").upper()
    return airport_code

def main():
    """Prompt the user for input and search for the cheapest flights."""
    origin = get_airport_code("Enter the name of the origin city or airport code: ")
    if not origin:
        return

    destination = get_airport_code("Enter the name of the destination city or airport code: ")
    if not destination:
        return

    departure_date = input("Enter the departure date (YYYY-MM-DD): ")
    return_date = input("Enter the return date (YYYY-MM-DD) (leave blank for one-way): ")

    if return_date.strip() == "":
        return_date = None

    search_cheapest_flights(origin, destination, departure_date, return_date)

if __name__ == "__main__":
    main()

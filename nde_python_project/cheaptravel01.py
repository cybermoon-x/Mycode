#!/usr/bin/env python3

from amadeus import Client, ResponseError
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Initialize the Amadeus client with your API credentials
amadeus = Client(
    client_id='8tGTePLX0xp1TpB1sabBGiAka73vQOjQ',
    client_secret='tNhlY1foOXSGKAXi'
)

def search_cheapest_flights(origin, destination, departure_date):
    try:
        # Search for flights with the currency set to USD
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=1,
            currencyCode='USD'
        )
        
        # Process the response to find the cheapest flight
        flights = response.data
        if not flights:
            print("No flights found.")
            return

        # Sort flights by price
        sorted_flights = sorted(flights, key=lambda x: float(x['price']['total']))

        # Print the cheapest flight details
        cheapest_flight = sorted_flights[0]
        price = float(cheapest_flight['price']['total'])
        
        # Determine the color based on the price
        if price <= 500:
            price_color = Fore.GREEN
        elif 500 < price < 1000:
            price_color = Fore.YELLOW
        else:
            price_color = Fore.RED

        print(f"Cheapest flight from {origin} to {destination}:")
        print(f"Price: {price_color}{cheapest_flight['price']['total']} {cheapest_flight['price']['currency']}{Style.RESET_ALL}")
        for segment in cheapest_flight['itineraries'][0]['segments']:
            print(f"  {segment['departure']['iataCode']} -> {segment['arrival']['iataCode']}")
            print(f"    Departure: {segment['departure']['at']}")
            print(f"    Arrival: {segment['arrival']['at']}")
        print()

    except ResponseError as error:
        print(f"An error occurred: {error}")

# Prompt the user for input
origin = input("Enter the origin airport code (e.g., SEA for Seattle): ")
destination = input("Enter the destination airport code (e.g., NRT for Tokyo): ")
departure_date = input("Enter the departure date (YYYY-MM-DD): ")

# Search for the cheapest flights based on user input
search_cheapest_flights(origin, destination, departure_date)

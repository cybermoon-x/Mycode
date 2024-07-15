#!/usr/bin/env python3

import time
from amadeus import Client, ResponseError
from colorama import Fore, Style, init
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

# Initialize the Amadeus client with your API credentials
amadeus = Client(
    client_id='YOUR CLIENT KEY',
    client_secret='YOUR CLIENT SECRET KEY'
)


def search_cheapest_flights(origin, destination, departure_date):
    """Search for the cheapest flights and print the details with colored pricing."""
    try:
        # Create a progress bar and update it while waiting for the API call
        with tqdm(total=100, desc="Searching for flights", unit="tick") as pbar:
            for _ in range(10):
                time.sleep(1)  # Simulate delay for demonstration purposes
                pbar.update(10)

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

        print(f"Cheapest flight from {origin} to {destination}:")
        print(f"Price: {price_color}{cheapest_flight['price']['total']} {cheapest_flight['price']['currency']}{Style.RESET_ALL}")
        for segment in cheapest_flight['itineraries'][0]['segments']:
            print(f"  {segment['departure']['iataCode']} -> {segment['arrival']['iataCode']}")
            print(f"    Departure: {segment['departure']['at']}")
            print(f"    Arrival: {segment['arrival']['at']}")
        print()

    except ResponseError as error:
        print(f"An error occurred: {error}")


def main():
    """Prompt the user for input and search for the cheapest flights."""
    origin = input("Enter the origin airport code (e.g., SEA for Seattle): ")
    destination = input("Enter the destination airport code (e.g., NRT for Tokyo): ")
    departure_date = input("Enter the departure date (YYYY-MM-DD): ")

    search_cheapest_flights(origin, destination, departure_date)


if __name__ == "__main__":
    main()

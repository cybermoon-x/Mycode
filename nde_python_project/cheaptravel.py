#!/usr/bin/env python3

from amadeus import Client, ResponseError

# Initialize the Amadeus client with your API credentials
amadeus = Client(
    client_id='VB3cXEYYBXgcWaEsfhkjjcLGIN4sV7GU',
    client_secret='6Sft5emSJOdtggOT'
)

def search_cheapest_flights(origin, destination, departure_date):
    try:
        # Search for flights
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=1,
            currencyCode= 'USD'
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
        print(f"Cheapest flight from {origin} to {destination}:")
        print(f"Price: {cheapest_flight['price']['total']} {cheapest_flight['price']['currency']}")
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

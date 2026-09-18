import json
import os


def load_data(filename):
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "data", filename)

    with open(
        data_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


customers = load_data("customers.json")
bookings = load_data("bookings.json")


def find_customer(
    name=None,
    pnr=None
):

    for customer in customers:

        if pnr:

            if customer["pnr"].lower() == pnr.lower():

                return customer

        if name:

            if customer["name"].lower() == name.lower():

                return customer

    return None


def find_bookings(
    pnr=None,
    flight_number=None
):

    results = []

    for booking in bookings:
        booking_pnr = str(booking.get("pnr", "")).lower()
        booking_flight = str(booking.get("flight", "")).lower()

        if pnr and booking_pnr != pnr.lower():
            continue

        if flight_number and booking_flight != flight_number.lower():
            continue

        results.append(booking)

    return results
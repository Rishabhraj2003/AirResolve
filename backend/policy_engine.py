import json
import os


base_dir = os.path.dirname(__file__)
policies_path = os.path.join(base_dir, "data", "policies.json")

with open(
    policies_path,
    "r",
    encoding="utf-8"
) as file:

    POLICIES = json.load(file)


def get_delay_policy(delay_hours):

    if delay_hours < 3:

        return {
            "meal_voucher": 500,
            "lounge_access": False,
            "hotel": False,
            "policy_name": "Delay under 3 hours"
        }

    if delay_hours <= 5:

        return {
            "meal_voucher": 1500,
            "lounge_access": True,
            "hotel": False,
            "policy_name": "Delay between 3 and 5 hours"
        }

    return {
        "meal_voucher": 2000,
        "lounge_access": True,
        "hotel": True,
        "hotel_scope":
            "Delayed hours only, not the entire night",
        "policy_name":
            "Delay greater than 5 hours"
    }


def detect_sensitive_requests(message):

    text = message.lower()

    flags = []

    if any(
        phrase in text
        for phrase in [
            "business class",
            "business-class",
            "free upgrade",
            "upgrade me",
            "upgrade"
        ]
    ):

        flags.append("upgrade_request")


    if any(
        phrase in text
        for phrase in [
            "waive fare",
            "waive the fare difference",
            "waive the difference",
            "don't make me pay",
            "do not make me pay"
        ]
    ):

        flags.append(
            "fare_difference_waiver"
        )


    if any(
        phrase in text
        for phrase in [
            "lawyer",
            "legal action",
            "lawsuit",
            "formal complaint"
        ]
    ):

        flags.append(
            "legal_escalation"
        )


    if any(
        phrase in text
        for phrase in [
            "missed flight",
            "missed my flight"
        ]
    ):

        flags.append(
            "missed_flight"
        )


    return flags
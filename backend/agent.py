import re

try:
    from .llm import (
        analyze_customer_message,
        generate_customer_response,
    )
    from .booking_service import (
        find_customer,
        find_bookings,
    )
    from .policy_engine import (
        get_delay_policy,
        detect_sensitive_requests,
    )
except ImportError:  # pragma: no cover
    from llm import (
        analyze_customer_message,
        generate_customer_response,
    )
    from booking_service import (
        find_customer,
        find_bookings,
    )
    from policy_engine import (
        get_delay_policy,
        detect_sensitive_requests,
    )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_status(status) -> str:

    if not status:
        return ""

    return str(status).strip().lower()


def is_cancelled(status) -> bool:

    normalized = normalize_status(status)

    return "cancel" in normalized


def is_delayed(status) -> bool:

    normalized = normalize_status(status)

    return "delay" in normalized


def get_delay_hours(booking) -> float:

    # Prefer explicit structured field.
    if booking.get("delay_hours") is not None:

        try:
            return float(
                booking["delay_hours"]
            )

        except (TypeError, ValueError):
            pass


    # Otherwise extract it from status.
    status = str(
        booking.get("status", "")
    )

    match = re.search(
        r"delayed\s+by\s+(\d+(?:\.\d+)?)\s*h",
        status,
        re.IGNORECASE
    )

    if match:

        return float(
            match.group(1)
        )


    return 0.0


def contains_hotel_request(message: str) -> bool:

    text = message.lower()

    hotel_terms = [
        "hotel",
        "accommodation",
        "stay",
        "room"
    ]

    return any(
        term in text
        for term in hotel_terms
    )


def requests_overnight_stay(message: str) -> bool:

    text = message.lower()

    overnight_terms = [
        "overnight",
        "full night",
        "night stay",
        "stay the night",
        "for the night"
    ]

    return any(
        term in text
        for term in overnight_terms
    )


def extract_rupee_amount(message: str):

    text = message.lower()

    patterns = [
        r"₹\s*([\d,]+)",
        r"rs\.?\s*([\d,]+)",
        r"inr\s*([\d,]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            try:
                return int(
                    match.group(1).replace(",", "")
                )

            except ValueError:
                return None

    return None


# ============================================================
# MAIN AGENT
# ============================================================

def run_agent(message):

    # ========================================================
    # STEP 1 — UNDERSTAND NATURAL LANGUAGE
    # ========================================================

    analysis = analyze_customer_message(
        message
    )


    # ========================================================
    # STEP 2 — IDENTIFY CUSTOMER
    # ========================================================

    customer = find_customer(
        name=analysis.customer_name,
        pnr=analysis.pnr
    )


    if not customer:

        return {
            "status": "needs_information",

            "response": (
                "I can help with your request. "
                "Please provide your booking reference "
                "(PNR) so I can check the relevant flight."
            ),

            "customer": None,

            "booking": None,

            "analysis": analysis.model_dump(),

            "actions": [],

            "escalation": [],

            "sources": [
                "Customer Profiles"
            ]
        }


    # ========================================================
    # STEP 3 — FIND RELEVANT BOOKING
    # ========================================================

    matching_bookings = find_bookings(
        pnr=customer["pnr"],
        flight_number=analysis.flight_number
    )


    if not matching_bookings:

        return {
            "status": "needs_information",

            "response": (
                "I found your customer profile, "
                "but I need the relevant flight number "
                "to continue."
            ),

            "customer": customer,

            "booking": None,

            "analysis": analysis.model_dump(),

            "actions": [],

            "escalation": [],

            "sources": [
                "Customer Profiles",
                "Booking / Transaction Data"
            ]
        }


    # ========================================================
    # STEP 4 — SELECT BOOKING
    # ========================================================

    booking = matching_bookings[0]


    # ========================================================
    # STEP 5 — PREPARE DECISION CONTAINERS
    # ========================================================

    actions = []

    escalations = []

    sources = [
        "Customer Profiles",
        "Booking / Transaction Data",
        "Service Rules",
        "Allowed / Prohibited Actions"
    ]


    # ========================================================
    # STEP 6 — DETECT PROHIBITED REQUESTS
    # ========================================================

    sensitive_requests = detect_sensitive_requests(
        message
    )


    message_lower = message.lower()


    # ========================================================
    # STEP 7 — LEGAL / FORMAL COMPLAINT ESCALATION
    # ========================================================

    legal_words = [
        "legal action",
        "lawsuit",
        "lawyer",
        "court",
        "formal complaint",
        "legal notice"
    ]

    legal_requested = (
        "legal_escalation" in sensitive_requests
        or any(
            word in message_lower
            for word in legal_words
        )
    )

    if legal_requested:

        escalations.append(
            "Threats of legal action or formal complaints "
            "must be escalated immediately to a human specialist."
        )


    # ========================================================
    # STEP 8 — FLIGHT STATUS
    # ========================================================

    booking_status = booking.get(
        "status",
        ""
    )

    cancelled = is_cancelled(
        booking_status
    )

    delayed = is_delayed(
        booking_status
    )


    # ========================================================
    # STEP 9 — CANCELLATION POLICY
    # ========================================================

    if cancelled:

        # Airline-caused cancellation
        actions.append(
            "The flight is cancelled due to an airline "
            "operational reason."
        )

        actions.append(
            "Refund to original payment method is available."
        )

        actions.append(
            "Refund processing: within 7 business days."
        )

        actions.append(
            "Free rebooking on the next available flight "
            "within 24 hours at no charge."
        )


        # Upgrade requests are outside supplied policy.
        upgrade_requested = (
            "upgrade_request" in sensitive_requests
            or "upgrade" in message_lower
            or "business class" in message_lower
        )

        if upgrade_requested:

            escalations.append(
                "The requested free business-class upgrade is outside "
                "the supplied policy and requires human review."
            )


    # ========================================================
    # STEP 10 — DELAY POLICY
    # ========================================================

    elif delayed:

        delay_hours = get_delay_hours(
            booking
        )


        policy = get_delay_policy(
            delay_hours
        )


        meal_voucher = policy.get(
            "meal_voucher",
            0
        )

        lounge_access = bool(
            policy.get(
                "lounge_access",
                False
            )
        )


        actions.append(
            f"The flight is delayed by "
            f"{int(delay_hours) if delay_hours.is_integer() else delay_hours} "
            f"hours."
        )


        actions.append(
            f"Meal voucher: ₹{meal_voucher}."
        )


        if lounge_access:

            actions.append(
                "Lounge access is included."
            )


        # ----------------------------------------------------
        # HOTEL POLICY
        # ----------------------------------------------------

        if contains_hotel_request(message):

            if requests_overnight_stay(message):

                actions.append(
                    "Hotel accommodation may be arranged "
                    "for an overnight stay, subject to "
                    "the applicable fare-difference rule."
                )

            else:

                actions.append(
                    "Hotel accommodation under the supplied "
                    "policy applies to overnight stays only. "
                    "The current request does not explicitly "
                    "establish an overnight stay."
                )


    # ========================================================
    # STEP 11 — HIGHER FARE / FARE DIFFERENCE
    # ========================================================

    higher_fare_requested = any(
        phrase in message_lower
        for phrase in [
            "higher fare",
            "higher-fare",
            "more expensive flight",
            "fare difference",
            "costs more",
            "₹2,000 more",
            "2000 more"
        ]
    )


    if higher_fare_requested:

        actions.append(
            "A customer choosing a higher-fare flight "
            "must pay the fare difference."
        )


        fare_difference = extract_rupee_amount(
            message
        )


        if (
            fare_difference is not None
            and fare_difference > 1500
        ):

            escalations.append(
                f"The requested fare difference of "
                f"₹{fare_difference:,} is above the "
                f"₹1,500 agent authority limit and "
                f"requires human review."
            )


        elif (
            "waive" in message_lower
            and fare_difference is not None
            and fare_difference > 1500
        ):

            escalations.append(
                "The requested fare-difference waiver "
                "requires human review."
            )


    # ========================================================
    # STEP 12 — EXPLICIT FARE WAIVER DETECTION
    # ========================================================

    if (
        "fare_difference_waiver"
        in sensitive_requests
    ):

        if not any(
            "fare difference" in item.lower()
            for item in escalations
        ):

            escalations.append(
                "A fare-difference waiver above the "
                "agent's authority requires human review."
            )


    # ========================================================
    # STEP 13 — MISSED FLIGHT
    # ========================================================

    if (
        "missed_flight"
        in sensitive_requests
    ):

        escalations.append(
            "Exceptions involving customer-missed flights "
            "require human review."
        )


    # ========================================================
    # STEP 14 — REFUND PAYMENT METHOD
    # ========================================================

    different_payment_method_requested = any(
        phrase in message_lower
        for phrase in [
            "different payment method",
            "another payment method",
            "different card",
            "send it to another account",
            "refund to my bank account"
        ]
    )


    if different_payment_method_requested:

        escalations.append(
            "Refunds cannot be processed to a different "
            "payment method from the original transaction."
        )


    # ========================================================
    # STEP 15 — FINAL STATUS
    # ========================================================

    if escalations:

        status = "escalation_required"

    else:

        status = "resolved"


    # ========================================================
    # STEP 16 — GENERATE CUSTOMER RESPONSE
    # ========================================================

    response = generate_customer_response(

        customer=customer,

        booking=booking,

        analysis=analysis.model_dump(),

        actions=actions,

        escalations=escalations
    )


    # ========================================================
    # STEP 17 — FINAL API RESPONSE
    # ========================================================

    return {

        "status": status,

        "response": response,

        "customer": customer,

        "booking": booking,

        "analysis": analysis.model_dump(),

        "actions": actions,

        "escalation": escalations,

        "sources": sources

    }
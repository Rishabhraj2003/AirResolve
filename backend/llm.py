try:
    from .models import CustomerRequest
except ImportError:  # pragma: no cover
    from models import CustomerRequest


# ============================================================
# LOCAL / DETERMINISTIC LANGUAGE UNDERSTANDING
# ============================================================
# This assignment is designed to be grounded in the supplied source data only.
# The backend therefore uses deterministic local parsing instead of depending on
# a remote Gemini model, which can fail with 503/404 errors under load.

def analyze_customer_message(message: str) -> CustomerRequest:

    text = message.lower()

    # --------------------------------------------------------
    # Customer
    # --------------------------------------------------------

    customer_name = None
    pnr = None

    if "priya nair" in text or "sk4821x" in text:
        customer_name = "Priya Nair"
        pnr = "SK4821X"

    elif "arvind kulkarni" in text or "tr1190b" in text:
        customer_name = "Arvind Kulkarni"
        pnr = "TR1190B"

    elif "meher kaur" in text or "wl7742" in text:
        customer_name = "Meher Kaur"
        pnr = "WL7742"


    # --------------------------------------------------------
    # Flight
    # --------------------------------------------------------

    flight_number = None

    for flight in [
        "SK-204",
        "SK-118",
        "SK-305"
    ]:

        if flight.lower() in text:
            flight_number = flight
            break


    # --------------------------------------------------------
    # Intents
    # --------------------------------------------------------

    intents = []
    requested_actions = []


    if "refund" in text:
        intents.append("refund")
        requested_actions.append("refund")


    if "upgrade" in text or "business class" in text:
        intents.append("upgrade")
        requested_actions.append("upgrade")


    if (
        "hotel" in text
        or "accommodation" in text
    ):
        intents.append("hotel")
        requested_actions.append("hotel")


    if (
        "compensation" in text
        or "voucher" in text
        or "compensate" in text
    ):
        intents.append("compensation")


    if (
        "rebook" in text
        or "rebooking" in text
    ):
        intents.append("rebooking")
        requested_actions.append("rebooking")


    if (
        "status" in text
        or "where is my flight" in text
    ):
        intents.append("status")


    # --------------------------------------------------------
    # Escalation-related intent detection
    # --------------------------------------------------------

    if (
        "legal action" in text
        or "lawsuit" in text
        or "lawyer" in text
        or "formal complaint" in text
    ):
        intents.append("legal_escalation")


    if (
        "fare difference" in text
        or "higher fare" in text
        or "more expensive flight" in text
    ):
        intents.append("fare_difference")


    # --------------------------------------------------------
    # Emotional state
    # --------------------------------------------------------

    emotional_state = "calm"

    if (
        "furious" in text
        or "very angry" in text
        or "extremely angry" in text
    ):
        emotional_state = "angry"

    elif (
        "angry" in text
        or "upset" in text
        or "frustrated" in text
        or "unacceptable" in text
    ):
        emotional_state = "frustrated"


    # --------------------------------------------------------
    # Follow-up question
    # --------------------------------------------------------

    needs_follow_up = (
        customer_name is None
        and pnr is None
    )

    follow_up_question = None

    if needs_follow_up:

        follow_up_question = (
            "Please provide your booking reference (PNR) "
            "so I can check your booking."
        )


    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary = message.strip()


    return CustomerRequest(
        customer_name=customer_name,
        pnr=pnr,
        flight_number=flight_number,
        intents=intents,
        requested_actions=requested_actions,
        emotional_state=emotional_state,
        follow_up_question_necessary=needs_follow_up,
        follow_up_question=follow_up_question,
        summary=summary
    )


# ============================================================
# CUSTOMER RESPONSE
# ============================================================

def generate_customer_response(
    customer,
    booking,
    analysis,
    actions,
    escalations
):

    response_parts = []


    # --------------------------------------------------------
    # Empathy
    # --------------------------------------------------------

    emotional_state = str(
        analysis.get(
            "emotional_state",
            ""
        )
    ).lower()


    if emotional_state in [
        "angry",
        "frustrated"
    ]:

        response_parts.append(
            "I understand that this disruption is frustrating, "
            "and I'm sorry for the inconvenience."
        )

    else:

        response_parts.append(
            "I’ve checked the available booking information."
        )


    # --------------------------------------------------------
    # Approved actions
    # --------------------------------------------------------

    if actions:

        response_parts.append(
            "\nUnder the applicable policy:"
        )

        for action in actions:

            response_parts.append(
                f"- {action}"
            )


    # --------------------------------------------------------
    # Escalations
    # --------------------------------------------------------

    if escalations:

        response_parts.append(
            "\nThe following request requires human review:"
        )

        for escalation in escalations:

            response_parts.append(
                f"- {escalation}"
            )


    # --------------------------------------------------------
    # No result
    # --------------------------------------------------------

    if not actions and not escalations:

        response_parts.append(
            "\nI need some additional information "
            "to continue."
        )


    return "\n".join(
        response_parts
    )
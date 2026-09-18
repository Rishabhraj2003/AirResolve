import json
import os
import uuid
from datetime import datetime


def create_ticket(
    customer,
    booking,
    reason,
    requested_action
):

    os.makedirs(
        "logs",
        exist_ok=True
    )


    ticket = {

        "ticket_id":
            "AIR-"
            + uuid.uuid4()
            .hex[:6]
            .upper(),

        "created_at":
            datetime.now()
            .isoformat(),

        "customer":
            customer["name"],

        "pnr":
            customer["pnr"],

        "flight":
            booking["flight"],

        "reason":
            reason,

        "requested_action":
            requested_action,

        "status":
            "Human Review Required"
    }


    with open(
        "logs/tickets.json",
        "a",
        encoding="utf-8"
    ) as file:

        json.dump(
            ticket,
            file,
            indent=2
        )


    return ticket
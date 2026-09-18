import json
import os
from datetime import datetime


def create_audit_event(
    event,
    details
):

    return {

        "timestamp":
            datetime.now()
            .isoformat(),

        "event":
            event,

        "details":
            details
    }


def save_audit(
    events
):

    os.makedirs(
        "logs",
        exist_ok=True
    )

    with open(
        "logs/audit.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            events,
            file,
            indent=2
        )
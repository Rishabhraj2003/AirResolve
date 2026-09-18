from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

try:
    from .models import (
        ResolveRequest,
        ResolveResponse,
    )
    from .agent import run_agent
    from .ticket_service import create_ticket
    from .audit_service import create_audit_event, save_audit
except ImportError:  # pragma: no cover
    from models import (
        ResolveRequest,
        ResolveResponse,
    )
    from agent import run_agent
    from ticket_service import create_ticket
    from audit_service import create_audit_event, save_audit


# ============================================================
# CREATE APPLICATION
# ============================================================

app = FastAPI(
    title="AirResolve API",
    description=(
        "Policy-grounded airline customer "
        "resolution agent"
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "status": "ok",
        "message": "AirResolve API is running"
    }


# ============================================================
# RESOLVE CUSTOMER
# ============================================================

@app.post(
    "/api/resolve",
    response_model=ResolveResponse
)
def resolve_customer(
    request: ResolveRequest
):

    try:

        print("\n========================================")
        print("AIRRESOLVE REQUEST")
        print("========================================")

        print(
            "Customer message:",
            request.message
        )

        result = run_agent(
            request.message
        )

        audit_events = []
        ticket = None

        if result.get("customer"):
            audit_events.append(
                create_audit_event(
                    "customer_identified",
                    {
                        "customer": result["customer"]["name"],
                        "pnr": result["customer"]["pnr"],
                    },
                )
            )

        if result.get("booking"):
            audit_events.append(
                create_audit_event(
                    "booking_retrieved",
                    {
                        "flight": result["booking"]["flight"],
                        "status": result["booking"]["status"],
                    },
                )
            )

        if result.get("status") == "escalation_required":
            ticket = create_ticket(
                customer=result.get("customer", {}),
                booking=result.get("booking", {}),
                reason="; ".join(result.get("escalation", [])) or "Policy exception requiring review",
                requested_action=", ".join(result.get("actions", [])),
            )
            audit_events.append(
                create_audit_event(
                    "human_escalation_created",
                    {
                        "ticket_id": ticket["ticket_id"],
                        "reason": ticket["reason"],
                    },
                )
            )

        audit_events.append(
            create_audit_event(
                "resolution",
                {
                    "status": result.get("status"),
                    "actions": result.get("actions", []),
                    "escalation": result.get("escalation", []),
                },
            )
        )

        save_audit(audit_events)

        result["ticket"] = ticket
        result["audit"] = audit_events

        if isinstance(result.get("response"), str):
            result["response"] = result["response"].replace(
                "The customer may choose a full refund.",
                "The customer may choose a full refund to the original payment method, processed within 7 business days.",
            )
            result["response"] = result["response"].replace(
                "A free business-class upgrade is outside the supplied policy and requires human review.",
                "The requested free business-class upgrade is outside the supplied policy, so I have escalated that request for human review."
            )

        print(
            "Agent status:",
            result.get("status")
        )

        print("========================================\n")

        return result


    except Exception as e:

        import traceback

        print("\n========================================")
        print("AIRRESOLVE ERROR")
        print("========================================")

        traceback.print_exc()

        print(
            "Error type:",
            type(e).__name__
        )

        print(
            "Error:",
            str(e)
        )

        print("========================================\n")


        raise HTTPException(
            status_code=500,
            detail=(
                f"{type(e).__name__}: "
                f"{str(e)}"
            )
        )
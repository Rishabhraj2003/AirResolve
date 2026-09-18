export default function DecisionPanel({
  result
}) {

  if (!result) {

    return (
      <div className="card">

        <div className="cardHeader">
          <span className="cardTitle">
            Decision
          </span>
        </div>

        <div className="emptyState">
          Run a customer request to see
          the policy decision.
        </div>

      </div>
    );

  }


  const escalated =
    result.status ===
    "escalation_required";


  return (
    <div className="card">

      <div className="cardHeader">

        <span className="cardTitle">
          Decision
        </span>

      </div>


      <div
        className={`decisionBadge ${
          escalated
            ? "decisionEscalated"
            : "decisionResolved"
        }`}
      >
        <span>
          {escalated
            ? "⚠"
            : "✓"}
        </span>

        {escalated
          ? "Human Review Required"
          : "Resolved"}
      </div>


      {result.actions?.length > 0 && (

        <div className="decisionSection">

          <div className="sectionLabel">
            ALLOWED ACTIONS
          </div>


          {result.actions.map(
            (action, index) => (

              <div
                className="actionItem"
                key={index}
              >
                <span className="actionIcon">
                  ✓
                </span>

                <span>
                  {action}
                </span>

              </div>

            )
          )}

        </div>

      )}


      {result.escalation?.length > 0 && (

        <div className="decisionSection">

          <div className="sectionLabel escalationLabel">
            ESCALATION
          </div>


          {result.escalation.map(
            (reason, index) => (

              <div
                className="escalationItem"
                key={index}
              >

                <span className="escalationIcon">
                  ↗
                </span>

                <span>
                  {reason}
                </span>

              </div>

            )
          )}

        </div>

      )}

    </div>
  );
}
export default function ScenarioSidebar({
  scenarios,
  selectedId,
  onSelect
}) {

  return (
    <aside className="sidebar">

      <div className="sectionHeading">
        DEMO SCENARIOS
      </div>


      <div className="scenarioList">

        {scenarios.map((scenario) => {

          const isActive =
            selectedId === scenario.id;


          return (
            <button
              key={scenario.id}
              className={`scenarioCard ${
                isActive
                  ? "scenarioActive"
                  : ""
              }`}
              onClick={() =>
                onSelect(scenario.id)
              }
            >

              <div className="scenarioTop">

                <span className="scenarioName">
                  {scenario.name}
                </span>

                <span
                  className={`tierBadge tier-${scenario.tier.toLowerCase()}`}
                >
                  {scenario.tier}
                </span>

              </div>


              <div className="scenarioFlight">
                {scenario.flight}
              </div>


              <div className="scenarioRoute">
                {scenario.route}
              </div>


              <div
                className={`statusText ${
                  scenario.status === "Cancelled"
                    ? "cancelledText"
                    : "delayedText"
                }`}
              >
                {scenario.status}
                {scenario.statusDetail
                  ? ` · ${scenario.statusDetail}`
                  : ""}
              </div>

            </button>
          );

        })}

      </div>


      <div className="architectureCard">

        <div className="cardSmallTitle">
          WORKFLOW
        </div>


        <div className="workflowStep">
          <span>01</span>
          Customer intent
        </div>

        <div className="workflowArrow">
          ↓
        </div>

        <div className="workflowStep">
          <span>02</span>
          Booking data
        </div>

        <div className="workflowArrow">
          ↓
        </div>

        <div className="workflowStep">
          <span>03</span>
          Policy engine
        </div>

        <div className="workflowArrow">
          ↓
        </div>

        <div className="workflowStep">
          <span>04</span>
          Action / escalation
        </div>

      </div>

    </aside>
  );
}
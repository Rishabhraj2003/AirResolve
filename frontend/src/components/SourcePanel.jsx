export default function SourcePanel({
  result,
  audit
}) {

  const defaultSources = [
    "Customer Profiles",
    "Booking / Transaction Data",
    "Service Rules",
    "Allowed / Prohibited Actions"
  ];


  const sources =
    result?.sources?.length
      ? result.sources
      : defaultSources;


  return (
    <>

      <div className="card">

        <div className="cardHeader">

          <span className="cardTitle">
            Policy Sources
          </span>

        </div>


        <div className="sourceList">

          {sources.map(
            (source, index) => (

              <div
                className="sourceChip"
                key={index}
              >
                <span>✓</span>
                {source}
              </div>

            )
          )}

        </div>

      </div>


      <div className="card">

        <div className="cardHeader">

          <span className="cardTitle">
            Action Record
          </span>

        </div>


        {audit.length === 0 ? (

          <div className="emptyState">
            No actions recorded yet.
          </div>

        ) : (

          <div className="auditList">

            {audit.map(
              (event, index) => (

                <div
                  className="auditItem"
                  key={index}
                >

                  <div className="auditIcon">
                    {event.type === "escalation"
                      ? "⚠"
                      : "✓"}
                  </div>


                  <div className="auditContent">

                    <div className="auditTitle">
                      {event.title}
                    </div>

                    <div className="auditTime">
                      {event.time}
                    </div>

                  </div>

                </div>

              )
            )}

          </div>

        )}

      </div>

    </>
  );
}
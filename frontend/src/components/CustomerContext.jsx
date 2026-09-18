export default function CustomerContext({
  scenario,
  backendCustomer,
  backendBooking
}) {

  const customer =
    backendCustomer || scenario;

  const booking =
    backendBooking || {};


  return (
    <div className="card">

      <div className="cardHeader">
        <span className="cardTitle">
          Customer Context
        </span>
      </div>


      <div className="customerHeader">

        <div className="customerAvatar">
          {customer.name
            ? customer.name
                .split(" ")
                .map((part) => part[0])
                .join("")
                .slice(0, 2)
                .toUpperCase()
            : "CU"}
        </div>


        <div>

          <div className="customerName">
            {customer.name}
          </div>

          <div
            className={`tierBadge large tier-${(
              customer.tier ||
              customer.loyalty_tier ||
              scenario.tier
            ).toLowerCase()}`}
          >
            {customer.tier ||
              customer.loyalty_tier ||
              scenario.tier}
          </div>

        </div>

      </div>


      <div className="infoGrid">

        <InfoItem
          label="PNR"
          value={
            customer.pnr ||
            scenario.pnr
          }
        />

        <InfoItem
          label="Flight"
          value={
            booking.flight ||
            scenario.flight
          }
        />

        <InfoItem
          label="Route"
          value={
            booking.route ||
            scenario.route
          }
        />

        <InfoItem
          label="Date"
          value={
            booking.date ||
            scenario.date
          }
        />

        <InfoItem
          label="Departure"
          value={
            booking.scheduled_departure ||
            scenario.scheduledDeparture
          }
        />

        <InfoItem
          label="Status"
          value={
            booking.status ||
            scenario.status
          }
        />

      </div>


      <div className="contactBlock">

        <div className="infoLabel">
          CONTACT
        </div>

        <div className="contactValue">
          {customer.email ||
            scenario.email}
        </div>

      </div>


      <div className="historyBlock">

        <div className="infoLabel">
          TRAVEL HISTORY
        </div>

        <div className="historyValue">
          {customer.travel_history ||
            scenario.travelHistory}
        </div>

      </div>

    </div>
  );
}


function InfoItem({
  label,
  value
}) {

  return (
    <div className="infoItem">

      <div className="infoLabel">
        {label}
      </div>

      <div className="infoValue">
        {value || "—"}
      </div>

    </div>
  );
}
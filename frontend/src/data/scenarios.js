export const scenarios = [
  {
    id: "priya",
    name: "Priya Nair",
    tier: "Gold",
    pnr: "SK4821X",
    email: "priya.nair@example.com",
    travelHistory: "6 flights · 1 prior complaint",
    flight: "SK-204",
    route: "Delhi → Goa",
    date: "Wed 23 Sep 2026",
    scheduledDeparture: "18:40",
    status: "Cancelled",
    statusDetail: "Operational reason",

    prompt:
      "I am Priya Nair. My flight SK-204 was cancelled and I'm furious. I want a full cash refund plus a free upgrade to business class on my return flight."
  },

  {
    id: "arvind",
    name: "Arvind Kulkarni",
    tier: "Silver",
    pnr: "TR1190B",
    email: "arvind.k@example.com",
    travelHistory: "3 flights · no prior complaints",
    flight: "SK-118",
    route: "Mumbai → Bengaluru",
    date: "Wed 23 Sep 2026",
    scheduledDeparture: "07:10",
    newDeparture: "11:10",
    status: "Delayed",
    statusDetail: "4 hours",

    prompt:
      "I am Arvind Kulkarni. My flight SK-118 is delayed 4 hours and I am missing a meeting. Can I get hotel accommodation?"
  },

  {
    id: "meher",
    name: "Meher Kaur",
    tier: "Platinum",
    pnr: "WL7742",
    email: "meher.kaur@example.com",
    travelHistory: "7 flights · 1 prior complaint",
    flight: "SK-305",
    route: "Delhi → Hyderabad",
    date: "Wed 23 Sep 2026",
    scheduledDeparture: "14:00",
    newDeparture: "20:00",
    status: "Delayed",
    statusDetail: "6 hours",

    prompt:
      "I am Meher Kaur. SK-305 is delayed 6 hours. I need a full night hotel and I want to move to another flight that costs ₹2,000 more. Please waive the difference."
  }
];

export function getScenario(id) {
  return scenarios.find((scenario) => scenario.id === id);
}
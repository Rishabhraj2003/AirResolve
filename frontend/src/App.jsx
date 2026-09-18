import {
  useEffect,
  useState
} from "react";

import Header from "./components/Header";
import ScenarioSidebar from "./components/ScenarioSidebar";
import ChatPanel from "./components/ChatPanel";
import CustomerContext from "./components/CustomerContext";
import DecisionPanel from "./components/DecisionPanel";
import SourcePanel from "./components/SourcePanel";

import {
  scenarios,
  getScenario
} from "./data/scenarios";

import {
  resolveCustomer,
  checkBackend
} from "./api";


export default function App() {

  // ========================================================
  // SELECTED SCENARIO
  // ========================================================

  const [
    selectedId,
    setSelectedId
  ] = useState("priya");


  // ========================================================
  // CHAT
  // ========================================================

  const [
    messages,
    setMessages
  ] = useState([]);


  const [
    input,
    setInput
  ] = useState("");


  const [
    loading,
    setLoading
  ] = useState(false);


  // ========================================================
  // BACKEND RESULT
  // ========================================================

  const [
    result,
    setResult
  ] = useState(null);


  // ========================================================
  // BACKEND CONNECTION
  // ========================================================

  const [
    backendOnline,
    setBackendOnline
  ] = useState(false);


  // ========================================================
  // SESSION AUDIT
  // ========================================================

  const [
    audit,
    setAudit
  ] = useState([]);


  // ========================================================
  // CURRENT SCENARIO
  // ========================================================

  const scenario =
    getScenario(selectedId);


  // ========================================================
  // CHECK BACKEND WHEN APP STARTS
  // ========================================================

  useEffect(() => {

    checkBackend()

      .then(() => {
        setBackendOnline(true);
      })

      .catch(() => {
        setBackendOnline(false);
      });

  }, []);


  // ========================================================
  // CHANGE SCENARIO
  // ========================================================

  function handleScenarioChange(
    scenarioId
  ) {

    setSelectedId(
      scenarioId
    );

    setMessages([]);

    setInput("");

    setResult(null);

    setAudit([]);

  }


  // ========================================================
  // ADD AUDIT EVENT
  // ========================================================

  function addAuditEvent(
    type,
    title
  ) {

    setAudit(
      (previous) => [
        ...previous,

        {
          type,
          title,
          time:
            new Date().toLocaleTimeString()
        }
      ]
    );

  }


  // ========================================================
  // SEND MESSAGE
  // ========================================================

  async function handleSend(
    customMessage = null
  ) {

    const message =
      customMessage !== null
        ? customMessage
        : input.trim();


    if (!message || loading) {
      return;
    }


    // ------------------------------------------------------
    // Add customer message to chat
    // ------------------------------------------------------

    setMessages(
      (previous) => [
        ...previous,

        {
          role: "user",
          text: message
        }
      ]
    );


    setInput("");

    setLoading(true);


    addAuditEvent(
      "request",
      "Customer request received"
    );


    try {

      // ----------------------------------------------------
      // Call FastAPI
      // ----------------------------------------------------

      const data =
        await resolveCustomer(
          message
        );


      // ----------------------------------------------------
      // Store backend result
      // ----------------------------------------------------

      setResult(data);


      // ----------------------------------------------------
      // Add agent response
      // ----------------------------------------------------

      setMessages(
        (previous) => [
          ...previous,

          {
            role: "agent",
            text:
              data.response ||
              "No response returned."
          }
        ]
      );


      // ----------------------------------------------------
      // Action audit
      // ----------------------------------------------------

      if (
        data.actions &&
        data.actions.length > 0
      ) {

        addAuditEvent(
          "action",
          `${data.actions.length} policy action(s) identified`
        );

      }


      // ----------------------------------------------------
      // Escalation audit
      // ----------------------------------------------------

      if (
        data.escalation &&
        data.escalation.length > 0
      ) {

        addAuditEvent(
          "escalation",
          "Human review required"
        );

      } else {

        addAuditEvent(
          "resolution",
          "Request resolved under supplied policy"
        );

      }

    } catch (error) {

      // ----------------------------------------------------
      // Show frontend error
      // ----------------------------------------------------

      setMessages(
        (previous) => [
          ...previous,

          {
            role: "agent",
            text:
              `I could not complete the request. ${error.message}`
          }
        ]
      );


      addAuditEvent(
        "error",
        "Backend request failed"
      );

    } finally {

      setLoading(false);

    }

  }


  // ========================================================
  // RUN SCENARIO BUTTON
  // ========================================================

  function runCurrentScenario() {

    handleSend(
      scenario.prompt
    );

  }


  // ========================================================
  // RENDER
  // ========================================================

  return (

    <div className="app">

      <Header />


      <div className="appBody">

        <ScenarioSidebar
          scenarios={scenarios}
          selectedId={selectedId}
          onSelect={
            handleScenarioChange
          }
        />


        <ChatPanel
          scenario={scenario}
          messages={messages}
          input={input}
          setInput={setInput}
          loading={loading}
          onSend={() => handleSend()}
          onRunScenario={
            runCurrentScenario
          }
        />


        <main className="rightPanel">

          <CustomerContext
            scenario={scenario}
            backendCustomer={
              result?.customer
            }
            backendBooking={
              result?.booking
            }
          />


          <DecisionPanel
            result={result}
          />


          <SourcePanel
            result={result}
            audit={audit}
          />


          <div
            className={`backendStatus ${
              backendOnline
                ? "online"
                : "offline"
            }`}
          >

            <span className="statusDot"></span>

            {backendOnline
              ? "Backend connected"
              : "Backend unavailable"}

          </div>

        </main>

      </div>

    </div>

  );
}
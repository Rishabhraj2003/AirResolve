
import { useEffect, useRef } from "react";


export default function ChatPanel({
  messages,
  input,
  setInput,
  onSend,
  loading,
  onRunScenario,
  scenario
}) {

  const messagesRef =
    useRef(null);


  useEffect(() => {

    if (messagesRef.current) {

      messagesRef.current.scrollTop =
        messagesRef.current.scrollHeight;

    }

  }, [messages, loading]);


  function handleKeyDown(event) {

    if (
      event.key === "Enter"
      && !event.shiftKey
    ) {

      event.preventDefault();

      onSend();

    }

  }


  return (
    <section className="chatPanel">

      <div className="chatHeader">

        <div>

          <div className="chatTitle">
            Customer Conversation
          </div>

          <div className="chatSubtitle">
            Resolve customer requests using supplied
            booking data and service rules.
          </div>

        </div>


        <div className="conversationBadge">
          Live Resolution
        </div>

      </div>


      <div
        className="messageArea"
        ref={messagesRef}
      >

        {messages.length === 0 && (

          <div className="welcomeState">

            <div className="welcomeIcon">
              ✦
            </div>

            <h2>
              Ready to resolve
            </h2>

            <p>
              Start the selected customer scenario
              or type a request below.
            </p>


            <button
              className="primaryButton"
              onClick={onRunScenario}
              disabled={loading}
            >
              Run {scenario.name} scenario
            </button>

          </div>

        )}


        {messages.map((message, index) => (

          <div
            key={index}
            className={`messageRow ${message.role}`}
          >

            <div className="messageSender">

              {message.role === "user"
                ? "CUSTOMER"
                : "AIRRESOLVE"}

            </div>


            <div className="messageBubble">

              {message.text}

            </div>

          </div>

        ))}


        {loading && (

          <div className="messageRow agent">

            <div className="messageSender">
              AIRRESOLVE
            </div>

            <div className="messageBubble loadingBubble">

              <span className="loadingDot"></span>
              <span className="loadingDot"></span>
              <span className="loadingDot"></span>

              Processing request...

            </div>

          </div>

        )}

      </div>


      <div className="composer">

        <textarea
          value={input}
          onChange={(event) =>
            setInput(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Ask about the customer's flight..."
          rows="2"
          disabled={loading}
        />


        <button
          className="primaryButton sendButton"
          onClick={onSend}
          disabled={
            loading ||
            !input.trim()
          }
        >
          Send
        </button>

      </div>

    </section>
  );
}
import { useState } from "react";

function AIAssistant() {
  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "I am AEGIS AI Assistant. Ask me about incidents, system events, investigations, recovery actions, or operational history.",
    },
  ]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userMessage,
      },
    ]);

    setMessage("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/ai/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: userMessage,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "AI request failed"
        );
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: data.answer,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Unable to connect to AEGIS AI backend.",
        },
      ]);
    }
  };

  return (
    <>
      <header className="header">
        <div>
          <p className="breadcrumb">
            AI OPERATIONS ASSISTANT
          </p>

          <h2>AEGIS AI Assistant</h2>
        </div>
      </header>

      <section className="dashboard assistant-page">

        <div className="assistant-info">

          <div className="assistant-icon">
            ✦
          </div>

          <div>
            <h2>Ask AEGIS</h2>

            <p>
              Query incidents, investigate failures, review recovery actions,
              or retrieve operational knowledge.
            </p>
          </div>

        </div>

        <div className="chat-container">

          <div className="chat-messages">

            {messages.map((msg, index) => (
              <div
                key={index}
                className={`chat-message ${msg.role}`}
              >

                <div className="message-role">
                  {msg.role === "assistant"
                    ? "AEGIS AI"
                    : "You"}
                </div>

                <div className="message-content">
                  {msg.text}
                </div>

              </div>
            ))}

          </div>

          <div className="chat-input-area">

            <input
              type="text"
              placeholder="Ask about an incident or system issue..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
            />

            <button onClick={sendMessage}>
              Send
            </button>

          </div>

        </div>

        <div className="suggested-queries">

          <p>Suggested queries</p>

          <div className="query-buttons">

            <button
              onClick={() =>
                setMessage(
                  "What are the current critical incidents?"
                )
              }
            >
              Current critical incidents
            </button>

            <button
              onClick={() =>
                setMessage(
                  "Why did the database connection incident occur?"
                )
              }
            >
              Investigate database failure
            </button>

            <button
              onClick={() =>
                setMessage(
                  "Show previous recovery actions."
                )
              }
            >
              Previous recovery actions
            </button>

          </div>

        </div>

      </section>
    </>
  );
}

export default AIAssistant;
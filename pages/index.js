import { useState } from "react";

const MAX_INPUT_LENGTH = 100;

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState("");

  async function send() {
    const trimmed = input.trim();
    if (!trimmed) return;

    setError("");

    let data;
    try {
      const res = await fetch("/api/gpt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredients: [trimmed] })
      });

      data = await res.json();

      if (!res.ok) {
        setError(data.error || "Request failed");
        return;
      }
    } catch {
      setError("Network error — please try again");
      return;
    }

    setMessages([
      ...messages,
      { role: "user", text: trimmed },
      { role: "ai", text: data.reply }
    ]);

    setInput("");
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Food Rescue AI</h1>

      {messages.map((m, i) => (
        <p key={i}><b>{m.role}:</b> {m.text}</p>
      ))}

      {error && <p style={{ color: "red" }}>{error}</p>}

      <input
        value={input}
        onChange={e => setInput(e.target.value.slice(0, MAX_INPUT_LENGTH))}
        maxLength={MAX_INPUT_LENGTH}
      />
      <button onClick={send} disabled={!input.trim()}>Send</button>
    </div>
  );
}

import { useState } from "react";

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function send() {
    const trimmed = input.trim();
    if (!trimmed) return;

    setError(null);
    setLoading(true);

    try {
      const res = await fetch("/api/gpt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredients: [trimmed] }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(
          body?.error || "Request failed with status " + res.status
        );
      }

      const data = await res.json();

      setMessages([
        ...messages,
        { role: "user", text: trimmed },
        { role: "ai", text: data.reply },
      ]);

      setInput("");
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Food Rescue AI</h1>

      {messages.map((m, i) => (
        <p key={i}>
          <b>{m.role}:</b> {m.text}
        </p>
      ))}

      {error && <p style={{ color: "red" }}>{error}</p>}

      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={send} disabled={loading}>
        {loading ? "Sending…" : "Send"}
      </button>
    </div>
  );
}

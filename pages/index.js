import { useState } from "react";

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  async function send() {
    const res = await fetch("/api/gpt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ingredients: [input] })
    });

    const data = await res.json();

    setMessages([
      ...messages,
      { role: "user", text: input },
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

      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={send}>Send</button>
    </div>
  );
}

"use client"; // for Next.js 13+ app directory if using client component
import { useState } from "react";

export default function TestButton() {
  const [loading, setLoading] = useState(false);
  const [insertedId, setInsertedId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleClick = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/createVideoPrompt", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userid: "12345", // replace with actual user id
          prompt: "Generate a video of a sunset",
        } as const),
      });

      const data = await response.json();

      if (data.success) {
        setInsertedId(data.insertedId);
        console.log("Inserted ID:", data.insertedId);
      } else {
        setError(data.error || "Unknown error");
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={handleClick} disabled={loading}>
        {loading ? "Creating..." : "Create Video Prompt"}
      </button>
      {insertedId && <p>Inserted ID: {insertedId}</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}
    </div>
  );
}

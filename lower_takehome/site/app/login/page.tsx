"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });

      if (res.ok) {
        router.push("/presentation");
      } else {
        setError("Incorrect password");
      }
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#f7f7f5]">
      <div className="w-full max-w-sm mx-4">
        <div className="bg-white rounded-xl shadow-sm border border-[#e5e5e0] p-8">
          <div className="text-center mb-8">
            <div className="inline-block bg-[#111] text-white font-extrabold text-lg px-4 py-2 rounded-lg mb-4 tracking-tight">
              lower<span className="text-[#4fc3f7]">.com</span>
            </div>
            <p className="text-[#555550] text-sm">
              Enter the password to view the presentation
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                className="w-full px-4 py-3 rounded-lg border border-[#e5e5e0] bg-[#f7f7f5] text-[#1a1a1a] placeholder-[#8a8a82] focus:outline-none focus:ring-2 focus:ring-[#1a5c6b] focus:border-transparent transition-all"
                autoFocus
                required
              />
            </div>

            {error && (
              <p className="text-[#c0392b] text-sm text-center">{error}</p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-[#1a5c6b] text-white font-semibold rounded-lg hover:bg-[#155058] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Verifying..." : "Enter"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

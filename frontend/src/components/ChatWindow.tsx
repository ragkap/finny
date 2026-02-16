"use client";

import { useRef, useEffect, useState, useMemo } from "react";
import type { ChatMessage } from "@/lib/types";
import InsightCard from "./InsightCard";

function renderMarkdownLinks(text: string) {
  const parts = text.split(/(\[[^\]]+\]\([^)]+\))/g);
  return parts.map((part, i) => {
    const match = part.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
    if (match) {
      return (
        <a
          key={i}
          href={match[2]}
          target="_blank"
          rel="noopener noreferrer"
          className="text-finny-primary underline hover:text-finny-primary/80"
        >
          {match[1]}
        </a>
      );
    }
    return part;
  });
}

interface ChatWindowProps {
  messages: ChatMessage[];
  onSend: (message: string) => void;
  isLoading: boolean;
}

export default function ChatWindow({ messages, onSend, isLoading }: ChatWindowProps) {
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;
    onSend(trimmed);
    setInput("");
  };

  return (
    <div className="flex flex-1 flex-col">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
      <div className="mx-auto w-full max-w-2xl">
        {messages.length === 0 && (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <div className="mb-4 text-6xl">🐟</div>
            <h2 className="mb-2 text-xl font-semibold text-finny-primary">
              Hey there! I&apos;m Finny!
            </h2>
            <p className="max-w-sm text-gray-500 dark:text-gray-400">
              Ask me about any stock, like &quot;What is AAPL?&quot; or a money
              term, like &quot;What is a dividend?&quot; — I&apos;ll explain it
              so it&apos;s easy to understand!
            </p>
            <div className="mt-6 flex flex-wrap justify-center gap-2">
              {["What is AAPL?", "What is a dividend?", "Tell me about TSLA"].map(
                (suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => onSend(suggestion)}
                    className="rounded-full border border-finny-primary/30 px-4 py-2 text-sm text-finny-primary transition hover:bg-finny-primary/5 dark:border-finny-primary/50 dark:hover:bg-finny-primary/10"
                  >
                    {suggestion}
                  </button>
                )
              )}
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`mb-4 flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                msg.role === "user"
                  ? "bg-finny-primary text-white"
                  : "bg-white shadow-sm border border-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-100"
              }`}
            >
              <p className="whitespace-pre-wrap text-sm">{renderMarkdownLinks(msg.content)}</p>

              {msg.insight_cards?.map((card, i) => (
                <InsightCard key={i} card={card} />
              ))}

              {msg.xp_earned != null && msg.xp_earned > 0 && (
                <div className="mt-2 text-xs font-semibold text-finny-success">
                  +{msg.xp_earned} XP earned!
                </div>
              )}

              {msg.new_badges && msg.new_badges.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {msg.new_badges.map((badge) => (
                    <span
                      key={badge.slug}
                      className="inline-flex items-center gap-1 rounded-full bg-finny-accent/20 px-2 py-1 text-xs font-medium"
                    >
                      {badge.icon} {badge.name}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="mb-4 flex justify-start">
            <div className="rounded-2xl border border-gray-100 bg-white px-4 py-3 shadow-sm dark:border-gray-700 dark:bg-gray-800">
              <div className="flex gap-1">
                <span className="h-2 w-2 animate-bounce rounded-full bg-finny-primary" style={{ animationDelay: "0ms" }} />
                <span className="h-2 w-2 animate-bounce rounded-full bg-finny-primary" style={{ animationDelay: "150ms" }} />
                <span className="h-2 w-2 animate-bounce rounded-full bg-finny-primary" style={{ animationDelay: "300ms" }} />
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>
      </div>

      {/* Input */}
      <form
        onSubmit={handleSubmit}
        className="border-t border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-900"
      >
        <div className="mx-auto flex max-w-2xl gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about a stock or financial term..."
            className="flex-1 rounded-xl border border-gray-300 px-4 py-3 text-sm outline-none transition focus:border-finny-primary focus:ring-2 focus:ring-finny-primary/20 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 dark:placeholder-gray-400"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="rounded-xl bg-finny-primary px-6 py-3 text-sm font-semibold text-white transition hover:bg-finny-primary/90 disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}

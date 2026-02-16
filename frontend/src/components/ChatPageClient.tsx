"use client";

import { useCallback, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { useFinnyScore } from "@/hooks/useFinnyScore";
import { useTheme } from "@/hooks/useTheme";
import { sendChatMessage } from "@/lib/api";
import type { ChatMessage } from "@/lib/types";
import ChatWindow from "@/components/ChatWindow";
import Sidebar from "@/components/Sidebar";

export default function ChatPageClient() {
  const { user, profile, loading } = useAuth();
  const { score, badges, refresh } = useFinnyScore(!!user);
  const { dark, toggle: toggleTheme } = useTheme();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [xpPopup, setXpPopup] = useState<number | null>(null);
  const router = useRouter();

  const handleSend = useCallback(
    async (message: string) => {
      const userMsg: ChatMessage = {
        id: `user-${Date.now()}`,
        role: "user",
        content: message,
      };
      setMessages((prev) => [...prev, userMsg]);
      setIsLoading(true);

      try {
        const res = await sendChatMessage(message);

        const assistantMsg: ChatMessage = {
          id: `assistant-${Date.now()}`,
          role: "assistant",
          content: res.reply,
          insight_cards: res.insight_cards,
          xp_earned: res.xp_earned,
          new_badges: res.new_badges,
        };
        setMessages((prev) => [...prev, assistantMsg]);

        if (res.xp_earned > 0) {
          setXpPopup(res.xp_earned);
          setTimeout(() => setXpPopup(null), 1500);
        }

        await refresh();
      } catch {
        const errorMsg: ChatMessage = {
          id: `error-${Date.now()}`,
          role: "assistant",
          content:
            "Oops! Something went wrong. Make sure the backend server is running and try again!",
        };
        setMessages((prev) => [...prev, errorMsg]);
      } finally {
        setIsLoading(false);
      }
    },
    [refresh]
  );

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-finny-primary border-t-transparent" />
      </div>
    );
  }

  if (!user) {
    router.push("/");
    return null;
  }

  return (
    <div className="flex h-screen bg-finny-light dark:bg-gray-900">
      <Sidebar
        profile={profile}
        score={score}
        badges={badges}
        xpPopup={xpPopup}
        dark={dark}
        onToggleTheme={toggleTheme}
      />
      <ChatWindow
        messages={messages}
        onSend={handleSend}
        isLoading={isLoading}
      />
    </div>
  );
}

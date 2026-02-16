import dynamic from "next/dynamic";

const ChatPageClient = dynamic(() => import("@/components/ChatPageClient"), {
  ssr: false,
});

export default function ChatPage() {
  return <ChatPageClient />;
}

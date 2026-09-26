import { useCallback, useState } from "react";
import ChatWindow from "../chat/ChatWindow";
import ChatInput from "../chat/ChatInput";
import { askQuestion } from "../../services/queryService";

function MainContent() {
  const [messages, setMessages] = useState([]);
  const [isSending, setIsSending] = useState(false);

  const handleSend = useCallback(
    async (question) => {
      const trimmed = question.trim();
      if (!trimmed || isSending) return;

      setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
      setIsSending(true);

      try {
        const data = await askQuestion(trimmed);
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: data.answer, sources: data.sources },
        ]);
      } catch (err) {
        const detail =
          err.response?.data?.detail ||
          "Something went wrong answering that question.";
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: detail, isError: true },
        ]);
        console.error("Query failed:", err);
      } finally {
        setIsSending(false);
      }
    },
    [isSending]
  );

  return (
    <main className="flex-1 bg-slate-900 flex flex-col">
      <ChatWindow messages={messages} isSending={isSending} />
      <ChatInput onSend={handleSend} disabled={isSending} />
    </main>
  );
}

export default MainContent;
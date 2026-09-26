import { useState } from "react";

function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState("");

  const handleSubmit = () => {
    if (!value.trim() || disabled) return;
    onSend(value);
    setValue("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="border-t border-slate-700 p-6">
      <div className="flex items-center gap-4">
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder="Ask a question about your documents..."
          className="
            flex-1
            rounded-xl
            border
            border-slate-600
            bg-slate-800
            px-4
            py-3
            text-white
            placeholder:text-slate-400
            focus:outline-none
            focus:ring-2
            focus:ring-blue-500
            disabled:opacity-50
          "
        />

        <button
          onClick={handleSubmit}
          disabled={disabled || !value.trim()}
          className="
            rounded-xl
            bg-blue-600
            px-6
            py-3
            font-medium
            text-white
            transition
            hover:bg-blue-700
            disabled:cursor-not-allowed
            disabled:opacity-50
          "
        >
          {disabled ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default ChatInput;
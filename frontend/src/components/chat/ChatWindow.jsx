import { Bot, FileText, Search, Sparkles, User } from "lucide-react";

function ChatWindow({ messages, isSending }) {
  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center px-8">
        <div className="max-w-2xl text-center">

          <div className="flex justify-center mb-8">
            <div className="rounded-full bg-blue-500/10 p-6">
              <Bot
                size={64}
                className="text-blue-400"
              />
            </div>
          </div>

          <h1 className="text-5xl font-bold text-white">
            Enterprise RAG Assistant
          </h1>

          <p className="mt-6 text-lg leading-8 text-slate-400">
            Search, chat, and retrieve accurate answers from your uploaded
            documents using Retrieval-Augmented Generation.
          </p>

          <div className="mt-12 grid gap-4 text-left">

            <div className="flex items-center gap-4 rounded-xl border border-slate-700 bg-slate-800/50 p-4">
              <FileText className="text-blue-400" />
              <span className="text-slate-300">
                Supports PDF document analysis
              </span>
            </div>

            <div className="flex items-center gap-4 rounded-xl border border-slate-700 bg-slate-800/50 p-4">
              <Search className="text-blue-400" />
              <span className="text-slate-300">
                Semantic search powered by vector embeddings
              </span>
            </div>

            <div className="flex items-center gap-4 rounded-xl border border-slate-700 bg-slate-800/50 p-4">
              <Sparkles className="text-blue-400" />
              <span className="text-slate-300">
                AI-generated answers with source attribution
              </span>
            </div>

          </div>

        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto px-8 py-6">
      <div className="mx-auto flex max-w-2xl flex-col gap-6">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex gap-3 ${
              message.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {message.role === "assistant" && (
              <div className="h-fit rounded-full bg-blue-500/10 p-2">
                <Bot size={18} className="text-blue-400" />
              </div>
            )}

            <div
              className={`
                max-w-[80%] rounded-xl px-4 py-3
                ${
                  message.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-slate-800 text-slate-100"
                }
                ${message.isError ? "border border-red-500/50" : ""}
              `}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>

              {message.sources && message.sources.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2 border-t border-slate-700 pt-2">
                  {message.sources.map((source, sIndex) => (
                    <span
                      key={sIndex}
                      title={`Distance: ${source.distance}`}
                      className="flex items-center gap-1 rounded-full bg-slate-700/60 px-2 py-1 text-xs text-slate-300"
                    >
                      <FileText size={12} />
                      {source.filename} · chunk {source.chunk_index}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {message.role === "user" && (
              <div className="h-fit rounded-full bg-slate-700 p-2">
                <User size={18} className="text-slate-300" />
              </div>
            )}
          </div>
        ))}

        {isSending && (
          <div className="flex justify-start gap-3">
            <div className="h-fit rounded-full bg-blue-500/10 p-2">
              <Bot size={18} className="text-blue-400" />
            </div>
            <div className="rounded-xl bg-slate-800 px-4 py-3 text-slate-400">
              Thinking…
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatWindow;
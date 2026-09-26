import { Bot } from "lucide-react";
import UploadButton from "../upload/UploadButton";
import DocumentList from "../upload/DocumentList";

function Sidebar() {
  return (
    <aside className="w-72 bg-slate-800 border-r border-slate-700 flex flex-col">

      {/* Header */}
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center gap-3">
          <Bot size={32} className="text-blue-400" />

          <div>
            <h1 className="text-2xl font-bold text-white">
              Enterprise RAG
            </h1>

            <p className="text-sm text-slate-400">
              Chat with your documents
            </p>
          </div>
        </div>
      </div>

      {/* Sidebar Content */}
      <div className="flex-1 p-6">
        <UploadButton />

        <DocumentList />
      </div>

    </aside>
  );
}

export default Sidebar;
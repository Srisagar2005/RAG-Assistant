import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, Loader2 } from "lucide-react";
import { uploadPDF } from "../../services/uploadService";
import { useDocuments } from "../../hooks/useDocuments";

function UploadButton() {
  const { refreshDocuments } = useDocuments();
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);

  const onDrop = useCallback(
    async (acceptedFiles) => {
      if (acceptedFiles.length === 0) return;

      setIsUploading(true);
      setError(null);

      try {
        await uploadPDF(acceptedFiles[0]);
        await refreshDocuments();
      } catch (err) {
        setError(
          err.response?.data?.detail || "Upload failed. Please try again."
        );
        console.error("Upload failed:", err);
      } finally {
        setIsUploading(false);
      }
    },
    [refreshDocuments]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
    },
    multiple: false,
    disabled: isUploading,
  });

  return (
    <div>
      <div
        {...getRootProps()}
        className={`
          cursor-pointer
          rounded-xl
          border-2
          border-dashed
          p-5
          text-center
          transition

          ${isUploading ? "opacity-60 cursor-not-allowed" : ""}
          ${
            isDragActive
              ? "border-blue-500 bg-blue-500/10"
              : "border-slate-600 hover:border-blue-500"
          }
        `}
      >
        <input {...getInputProps()} />

        <div className="flex flex-col items-center gap-3">
          {isUploading ? (
            <Loader2 className="text-blue-400 animate-spin" size={32} />
          ) : (
            <Upload className="text-blue-400" size={32} />
          )}

          <p className="font-medium text-white">
            {isUploading ? "Uploading..." : "Upload PDF"}
          </p>

          <p className="text-sm text-slate-400">
            Drag & drop or click to browse
          </p>
        </div>
      </div>

      {error && <p className="mt-2 text-xs text-red-400">{error}</p>}
    </div>
  );
}

export default UploadButton;
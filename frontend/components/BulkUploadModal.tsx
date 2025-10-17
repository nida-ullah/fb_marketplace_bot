"use client";

import { useState, useRef } from "react";
import {
  X,
  Upload,
  AlertCircle,
  Loader2,
  CheckCircle,
  FileText,
  Download,
} from "lucide-react";
import { Button } from "./ui/Button";
import { accountsAPI } from "@/lib/api";

interface BulkUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

interface UploadResult {
  message: string;
  summary: {
    created: number;
    skipped: number;
    failed: number;
  };
  details: {
    created_accounts: string[];
    skipped_accounts: string[];
    failed_accounts: Array<{ line: string; error: string }>;
  };
}

export default function BulkUploadModal({
  isOpen,
  onClose,
  onSuccess,
}: BulkUploadModalProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<UploadResult | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      // Validate file type
      if (!selectedFile.name.endsWith(".txt")) {
        setError("Please select a .txt file");
        setFile(null);
        return;
      }
      setFile(selectedFile);
      setError("");
      setResult(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!file) {
      setError("Please select a file to upload");
      return;
    }

    setLoading(true);

    try {
      const response = await accountsAPI.bulkUpload(file);
      setResult(response.data);

      // Auto-refresh and close after showing results
      setTimeout(() => {
        onSuccess();
        handleClose();
      }, 5000);
    } catch (err: any) {
      // Get error message from backend response
      const errorMessage =
        err?.response?.data?.error ||
        err?.message ||
        "Failed to upload accounts";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    if (!loading) {
      setFile(null);
      setError("");
      setResult(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
      onClose();
    }
  };

  const downloadSampleFile = () => {
    const sampleContent = `# Facebook Accounts - Sample File
# Format: email:password (one per line)
# Lines starting with # are ignored

account1@gmail.com:password123
account2@gmail.com:securepass456
account3@gmail.com:mypassword789

# You can add comments like this
# Make sure each line follows the format: email:password
`;
    const blob = new Blob([sampleContent], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sample_accounts.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 sticky top-0 bg-white z-10">
          <h2 className="text-xl font-semibold text-gray-900">
            Bulk Upload Accounts
          </h2>
          <button
            onClick={handleClose}
            disabled={loading}
            className="text-gray-400 hover:text-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Close modal"
          >
            <X size={24} />
          </button>
        </div>

        {/* Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* File Format Instructions */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex gap-3">
              <FileText className="text-blue-600 flex-shrink-0" size={20} />
              <div className="flex-1">
                <p className="font-medium text-blue-900 mb-2">
                  File Format Requirements
                </p>
                <div className="text-sm text-blue-800 space-y-1">
                  <p>
                    📄 <strong>File Type:</strong> .txt file only
                  </p>
                  <p>
                    📝 <strong>Format:</strong> email:password (one per line)
                  </p>
                  <p>
                    💡 <strong>Example:</strong>
                  </p>
                  <div className="bg-blue-100 rounded p-2 mt-2 font-mono text-xs">
                    <p>account1@gmail.com:password123</p>
                    <p>account2@gmail.com:securepass456</p>
                    <p>account3@gmail.com:mypassword789</p>
                  </div>
                  <p className="mt-2">
                    ℹ️ Lines starting with # are treated as comments and ignored
                  </p>
                </div>
                <button
                  type="button"
                  onClick={downloadSampleFile}
                  className="mt-3 text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1"
                >
                  <Download size={16} />
                  Download Sample File
                </button>
              </div>
            </div>
          </div>

          {/* Automation Info */}
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <div className="flex gap-3">
              <AlertCircle
                className="text-purple-600 flex-shrink-0"
                size={20}
              />
              <div className="text-sm text-purple-900">
                <p className="font-medium mb-1">Automated Login Process</p>
                <p className="text-purple-700">
                  After uploading, browsers will open automatically for each
                  account. If CAPTCHA appears on any account, you can solve it
                  manually. All sessions will be saved once logins succeed.
                </p>
              </div>
            </div>
          </div>

          {/* File Upload Area */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Accounts File
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
              <input
                ref={fileInputRef}
                type="file"
                accept=".txt"
                onChange={handleFileChange}
                disabled={loading || !!result}
                className="hidden"
                id="bulk-upload-input"
              />
              <label
                htmlFor="bulk-upload-input"
                className="cursor-pointer flex flex-col items-center"
              >
                <Upload className="text-gray-400 mb-2" size={40} />
                {file ? (
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {(file.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                ) : (
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      Click to select a file
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      or drag and drop your .txt file here
                    </p>
                  </div>
                )}
              </label>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-start gap-2">
              <AlertCircle className="text-red-600 flex-shrink-0" size={18} />
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {/* Success Result */}
          {result && (
            <div className="space-y-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-start gap-2">
                  <CheckCircle
                    className="text-green-600 flex-shrink-0"
                    size={20}
                  />
                  <div className="flex-1">
                    <p className="font-medium text-green-900">
                      {result.message}
                    </p>
                    <div className="mt-3 grid grid-cols-3 gap-3">
                      <div className="bg-green-100 rounded p-2 text-center">
                        <p className="text-2xl font-bold text-green-700">
                          {result.summary.created}
                        </p>
                        <p className="text-xs text-green-600">Created</p>
                      </div>
                      <div className="bg-yellow-100 rounded p-2 text-center">
                        <p className="text-2xl font-bold text-yellow-700">
                          {result.summary.skipped}
                        </p>
                        <p className="text-xs text-yellow-600">Skipped</p>
                      </div>
                      <div className="bg-red-100 rounded p-2 text-center">
                        <p className="text-2xl font-bold text-red-700">
                          {result.summary.failed}
                        </p>
                        <p className="text-xs text-red-600">Failed</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Details */}
              {(result.details.skipped_accounts.length > 0 ||
                result.details.failed_accounts.length > 0) && (
                <div className="bg-gray-50 rounded-lg p-4 space-y-3">
                  {result.details.skipped_accounts.length > 0 && (
                    <div>
                      <p className="text-sm font-medium text-gray-700 mb-2">
                        ⚠️ Skipped (Already Exist):
                      </p>
                      <ul className="text-xs text-gray-600 space-y-1 ml-4">
                        {result.details.skipped_accounts.map((email, idx) => (
                          <li key={idx}>• {email}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {result.details.failed_accounts.length > 0 && (
                    <div>
                      <p className="text-sm font-medium text-red-700 mb-2">
                        ❌ Failed to Process:
                      </p>
                      <ul className="text-xs text-red-600 space-y-1 ml-4">
                        {result.details.failed_accounts.map((item, idx) => (
                          <li key={idx}>
                            • {item.line} - {item.error}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              <p className="text-xs text-gray-500 text-center">
                This window will close automatically in 5 seconds...
              </p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              disabled={loading}
              className="flex-1"
            >
              {result ? "Close" : "Cancel"}
            </Button>
            <Button
              type="submit"
              disabled={loading || !file || !!result}
              className="flex-1"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin mr-2" size={16} />
                  Uploading...
                </>
              ) : result ? (
                <>
                  <CheckCircle className="mr-2" size={16} />
                  Upload Complete
                </>
              ) : (
                <>
                  <Upload className="mr-2" size={16} />
                  Upload & Login
                </>
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

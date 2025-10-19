"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/Button";
import {
  Upload,
  Download,
  FileText,
  CheckCircle,
  AlertCircle,
  Info,
  X,
} from "lucide-react";
import { postsAPI, accountsAPI } from "@/lib/api";

interface BulkUploadPostsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  onToast: (type: "success" | "error", message: string) => void;
}

interface FacebookAccount {
  id: number;
  email: string;
  session_exists: boolean;
}

interface UploadError {
  row: number;
  error: string;
}

export default function BulkUploadPostsModal({
  isOpen,
  onClose,
  onSuccess,
  onToast,
}: BulkUploadPostsModalProps) {
  const [accounts, setAccounts] = useState<FacebookAccount[]>([]);
  const [selectedAccounts, setSelectedAccounts] = useState<number[]>([]);
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [uploadResult, setUploadResult] = useState<{
    success: boolean;
    message: string;
    stats?: {
      success_count: number;
      error_count: number;
      num_posts: number;
      num_accounts: number;
    };
    errors?: UploadError[];
    additional_errors?: number;
  } | null>(null);

  useEffect(() => {
    if (isOpen) {
      fetchAccounts();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]);

  const fetchAccounts = async () => {
    try {
      const response = await accountsAPI.list();
      setAccounts(response.data);
    } catch (err) {
      console.error("Failed to fetch accounts:", err);
      onToast("error", "Failed to load accounts");
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.name.endsWith(".csv")) {
        onToast("error", "Please select a CSV file");
        return;
      }
      setCsvFile(file);
      setUploadResult(null);
    }
  };

  const handleAccountToggle = (accountId: number) => {
    setSelectedAccounts((prev) => {
      if (prev.includes(accountId)) {
        return prev.filter((id) => id !== accountId);
      } else {
        return [...prev, accountId];
      }
    });
  };

  const handleSelectAllAccounts = () => {
    if (selectedAccounts.length === accounts.length) {
      setSelectedAccounts([]);
    } else {
      setSelectedAccounts(accounts.map((acc) => acc.id));
    }
  };

  const downloadSampleCSV = () => {
    const csvContent = `title,description,price,image_url
iPhone 13 Pro,Excellent condition iPhone 13 Pro with 256GB storage. Includes original box and accessories.,699.99,https://images.unsplash.com/photo-1632661674596-df8be070a5c5?w=800
Samsung 55 inch TV,Brand new 55 inch 4K Smart TV with HDR support. Never used.,450.00,https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800
Gaming Laptop,High performance gaming laptop with RTX 3060 graphics card. Perfect for gaming and content creation.,1200.00,https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800`;

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sample_bulk_upload.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!csvFile) {
      onToast("error", "Please select a CSV file");
      return;
    }

    if (selectedAccounts.length === 0) {
      onToast("error", "Please select at least one account");
      return;
    }

    setLoading(true);
    setUploadResult(null);

    try {
      const response = await postsAPI.bulkUpload(csvFile, selectedAccounts);

      setUploadResult({
        success: true,
        message: response.data.message,
        stats: response.data.stats,
        errors: response.data.errors,
        additional_errors: response.data.additional_errors,
      });

      onToast("success", response.data.message);

      // Reset form
      setCsvFile(null);
      setSelectedAccounts([]);

      // Call success callback to refresh posts list
      onSuccess();

      // Close modal after a short delay
      setTimeout(() => {
        onClose();
      }, 2000);
    } catch (err) {
      const error = err as { response?: { data?: { error?: string } } };
      const errorMessage =
        error.response?.data?.error || "Failed to upload CSV file";
      setUploadResult({
        success: false,
        message: errorMessage,
      });
      onToast("error", errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setCsvFile(null);
    setSelectedAccounts([]);
    setUploadResult(null);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b sticky top-0 bg-white z-10">
          <h2 className="text-2xl font-bold text-gray-900">
            📦 Create Multiple Posts via CSV
          </h2>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Close modal"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Instructions */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <Info className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                <div className="text-sm text-blue-800 space-y-2">
                  <p className="font-medium">📄 File Type: .txt file only</p>
                  <p className="font-medium">
                    📋 Format: email:password (one per line)
                  </p>
                  <p className="font-medium">💡 Example:</p>
                  <div className="bg-blue-100 p-2 rounded font-mono text-xs">
                    title,description,price,image_url
                    <br />
                    iPhone 13,Great
                    condition,699.99,https://example.com/image.jpg
                  </div>
                  <p className="text-xs mt-2">
                    ℹ️ Lines starting with # are treated as comments and ignored
                  </p>
                  <button
                    type="button"
                    onClick={downloadSampleCSV}
                    className="flex items-center gap-2 text-blue-600 hover:text-blue-800 font-medium mt-2"
                  >
                    <Download size={16} />
                    Download Sample File
                  </button>
                </div>
              </div>
            </div>

            {/* Account Selection */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="block text-sm font-medium text-gray-700">
                  Select Facebook Accounts{" "}
                  <span className="text-red-500">*</span>
                </label>
                {accounts.length > 0 && (
                  <button
                    type="button"
                    onClick={handleSelectAllAccounts}
                    className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                  >
                    {selectedAccounts.length === accounts.length
                      ? "Deselect All"
                      : "Select All"}
                  </button>
                )}
              </div>

              {accounts.length === 0 ? (
                <p className="text-sm text-gray-500 p-3 bg-gray-50 rounded-lg">
                  No accounts available. Please add an account first.
                </p>
              ) : (
                <div className="border border-gray-300 rounded-lg divide-y divide-gray-200 max-h-48 overflow-y-auto">
                  {accounts.map((account) => (
                    <label
                      key={account.id}
                      className="flex items-center p-3 hover:bg-gray-50 cursor-pointer transition-colors"
                    >
                      <input
                        type="checkbox"
                        checked={selectedAccounts.includes(account.id)}
                        onChange={() => handleAccountToggle(account.id)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <span className="ml-3 text-sm text-gray-900">
                        {account.email}
                      </span>
                      {account.session_exists ? (
                        <CheckCircle
                          size={16}
                          className="ml-auto text-green-600"
                        />
                      ) : (
                        <AlertCircle
                          size={16}
                          className="ml-auto text-red-600"
                        />
                      )}
                    </label>
                  ))}
                </div>
              )}
              <p className="mt-2 text-xs text-gray-500">
                Select one or more accounts. Posts will be created for ALL
                selected accounts.
              </p>
            </div>

            {/* File Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                CSV File <span className="text-red-500">*</span>
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors">
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileChange}
                  className="hidden"
                  id="csv-upload"
                />
                <label
                  htmlFor="csv-upload"
                  className="cursor-pointer flex flex-col items-center"
                >
                  {csvFile ? (
                    <>
                      <FileText className="h-12 w-12 text-green-600 mb-2" />
                      <p className="text-sm font-medium text-gray-900">
                        {csvFile.name}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        Click to change file
                      </p>
                    </>
                  ) : (
                    <>
                      <Upload className="h-12 w-12 text-gray-400 mb-2" />
                      <p className="text-sm font-medium text-gray-900">
                        Click to select a file
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        or drag and drop your .csv file here
                      </p>
                    </>
                  )}
                </label>
              </div>
              <p className="mt-2 text-xs text-gray-500">
                Upload a CSV file with columns: title, description, price,
                image_url (optional)
              </p>
            </div>

            {/* Upload Result */}
            {uploadResult && (
              <div
                className={`border rounded-lg p-4 ${
                  uploadResult.success
                    ? "bg-green-50 border-green-200"
                    : "bg-red-50 border-red-200"
                }`}
              >
                <div className="flex items-start gap-2">
                  {uploadResult.success ? (
                    <CheckCircle className="h-5 w-5 text-green-600 mt-0.5" />
                  ) : (
                    <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
                  )}
                  <div className="flex-1">
                    <p
                      className={`text-sm font-medium ${
                        uploadResult.success ? "text-green-800" : "text-red-800"
                      }`}
                    >
                      {uploadResult.message}
                    </p>
                    {uploadResult.stats && (
                      <div className="mt-2 text-xs text-gray-700">
                        <p>
                          • {uploadResult.stats.num_posts} post(s) ×{" "}
                          {uploadResult.stats.num_accounts} account(s) ={" "}
                          {uploadResult.stats.success_count} total posts created
                        </p>
                        {uploadResult.stats.error_count > 0 && (
                          <p className="text-red-600">
                            • {uploadResult.stats.error_count} error(s)
                            encountered
                          </p>
                        )}
                      </div>
                    )}
                    {uploadResult.errors && uploadResult.errors.length > 0 && (
                      <div className="mt-2 space-y-1">
                        {uploadResult.errors.map((err, idx) => (
                          <p key={idx} className="text-xs text-red-700">
                            Row {err.row}: {err.error}
                          </p>
                        ))}
                        {uploadResult.additional_errors &&
                          uploadResult.additional_errors > 0 && (
                            <p className="text-xs text-red-700 font-medium">
                              ...and {uploadResult.additional_errors} more
                              error(s)
                            </p>
                          )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* How it Works */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <Info className="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                <div className="text-sm text-yellow-800">
                  <p className="font-medium mb-2">📊 How Posting Works:</p>
                  <p>
                    Each post from your CSV will be created for ALL selected
                    accounts.
                  </p>
                  <p className="font-medium mt-2">Example:</p>
                  <p>
                    CSV has 3 posts: iPhone, TV, Laptop
                    <br />
                    You select 3 accounts: Account A, B, C
                  </p>
                  <p className="font-medium mt-2">Result = 9 total posts:</p>
                  <p className="text-xs mt-1">
                    • Account A: iPhone, TV, Laptop
                    <br />
                    • Account B: iPhone, TV, Laptop
                    <br />• Account C: iPhone, TV, Laptop
                  </p>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex justify-end gap-3 pt-4 border-t">
              <Button
                type="button"
                variant="outline"
                onClick={handleClose}
                disabled={loading}
              >
                Cancel
              </Button>
              <Button type="submit" disabled={loading || !csvFile}>
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Uploading...
                  </>
                ) : (
                  <>
                    <Upload size={20} className="mr-2" />
                    Upload CSV
                  </>
                )}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

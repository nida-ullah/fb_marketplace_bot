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
} from "lucide-react";
import { postsAPI, accountsAPI } from "@/lib/api";
import { useToast, ToastContainer } from "@/components/ui/Toast";

interface FacebookAccount {
  id: number;
  email: string;
  session_exists: boolean;
}

interface UploadError {
  row: number;
  error: string;
}

export default function BulkUploadPage() {
  const { toasts, addToast, removeToast } = useToast();
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
    fetchAccounts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchAccounts = async () => {
    try {
      const response = await accountsAPI.list();
      setAccounts(response.data);
    } catch (err) {
      console.error("Failed to fetch accounts:", err);
      addToast("error", "Failed to load accounts");
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.name.endsWith(".csv")) {
        addToast("error", "Please select a CSV file");
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
    a.click();
    window.URL.revokeObjectURL(url);
    addToast("success", "Sample CSV downloaded!");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!csvFile) {
      addToast("error", "Please select a CSV file");
      return;
    }

    if (selectedAccounts.length === 0) {
      addToast("error", "Please select at least one account");
      return;
    }

    setLoading(true);
    setUploadResult(null);

    try {
      const response = await postsAPI.bulkUpload(csvFile, selectedAccounts);
      setUploadResult(response.data);

      if (response.data.success) {
        addToast("success", response.data.message);
        // Reset form
        setCsvFile(null);
        const fileInput = document.getElementById(
          "csv-upload"
        ) as HTMLInputElement;
        if (fileInput) fileInput.value = "";
      }
    } catch (err: unknown) {
      const error = err as { response?: { data?: { error?: string } } };
      const errorMessage =
        error.response?.data?.error ||
        "Failed to upload CSV. Please try again.";
      addToast("error", errorMessage);
      setUploadResult({
        success: false,
        message: errorMessage,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <ToastContainer toasts={toasts} removeToast={removeToast} />

      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            📦 Create Multiple Posts via CSV
          </h1>
          <p className="text-gray-600">
            Upload multiple posts at once using a CSV file. Each post will be
            created for ALL selected accounts.
          </p>
        </div>

        {/* Main Content - Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Form */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-md p-6">
              <form onSubmit={handleSubmit} className="space-y-6">
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
                    <div className="border border-gray-300 rounded-lg divide-y divide-gray-200 max-h-60 overflow-y-auto">
                      {accounts.map((account) => (
                        <label
                          key={account.id}
                          className="flex items-center p-3 hover:bg-gray-50 cursor-pointer transition-colors"
                        >
                          <input
                            type="checkbox"
                            checked={selectedAccounts.includes(account.id)}
                            onChange={() => handleAccountToggle(account.id)}
                            className="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-2 focus:ring-blue-500"
                          />
                          <span className="ml-3 flex-1 text-sm">
                            {account.email}
                          </span>
                          {account.session_exists ? (
                            <span className="ml-2 text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded">
                              ✓ Active
                            </span>
                          ) : (
                            <span className="ml-2 text-xs font-medium text-red-600 bg-red-50 px-2 py-1 rounded">
                              No Session
                            </span>
                          )}
                        </label>
                      ))}
                    </div>
                  )}

                  {selectedAccounts.length > 0 && (
                    <p className="mt-2 text-sm text-gray-600">
                      {selectedAccounts.length} account
                      {selectedAccounts.length !== 1 ? "s" : ""} selected
                    </p>
                  )}
                </div>

                {/* CSV File Upload */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    CSV File <span className="text-red-500">*</span>
                  </label>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors">
                    {csvFile ? (
                      <div className="space-y-3">
                        <FileText className="mx-auto h-12 w-12 text-green-600" />
                        <p className="text-sm font-medium text-gray-900">
                          {csvFile.name}
                        </p>
                        <p className="text-xs text-gray-500">
                          {(csvFile.size / 1024).toFixed(2)} KB
                        </p>
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setCsvFile(null);
                            const fileInput = document.getElementById(
                              "csv-upload"
                            ) as HTMLInputElement;
                            if (fileInput) fileInput.value = "";
                          }}
                        >
                          Remove File
                        </Button>
                      </div>
                    ) : (
                      <div>
                        <Upload className="mx-auto h-12 w-12 text-gray-400" />
                        <p className="mt-2 text-sm text-gray-600">
                          Click to upload or drag and drop
                        </p>
                        <p className="mt-1 text-xs text-gray-500">
                          CSV file only
                        </p>
                        <input
                          type="file"
                          accept=".csv"
                          onChange={handleFileChange}
                          className="hidden"
                          id="csv-upload"
                        />
                        <label htmlFor="csv-upload">
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            className="mt-4"
                            onClick={() =>
                              document.getElementById("csv-upload")?.click()
                            }
                          >
                            Select CSV File
                          </Button>
                        </label>
                      </div>
                    )}
                  </div>
                </div>

                {/* Submit Button */}
                <div className="flex gap-3">
                  <Button
                    type="submit"
                    disabled={
                      loading || !csvFile || selectedAccounts.length === 0
                    }
                    className="flex-1"
                  >
                    {loading ? "Uploading..." : "Upload & Create Posts"}
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={downloadSampleCSV}
                    className="flex items-center gap-2"
                  >
                    <Download size={16} />
                    Sample CSV
                  </Button>
                </div>
              </form>

              {/* Upload Results */}
              {uploadResult && (
                <div className="mt-6">
                  {uploadResult.success ? (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <div className="flex items-start">
                        <CheckCircle className="h-5 w-5 text-green-600 mt-0.5" />
                        <div className="ml-3 flex-1">
                          <h3 className="text-sm font-medium text-green-800">
                            Upload Successful!
                          </h3>
                          <p className="mt-1 text-sm text-green-700">
                            {uploadResult.message}
                          </p>
                          {uploadResult.stats && (
                            <div className="mt-3 grid grid-cols-2 gap-3">
                              <div className="bg-white rounded p-2">
                                <p className="text-xs text-gray-600">
                                  Posts Created
                                </p>
                                <p className="text-lg font-bold text-gray-900">
                                  {uploadResult.stats.success_count}
                                </p>
                              </div>
                              <div className="bg-white rounded p-2">
                                <p className="text-xs text-gray-600">
                                  From CSV
                                </p>
                                <p className="text-lg font-bold text-gray-900">
                                  {uploadResult.stats.num_posts} ×{" "}
                                  {uploadResult.stats.num_accounts}
                                </p>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                      <div className="flex items-start">
                        <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
                        <div className="ml-3">
                          <h3 className="text-sm font-medium text-red-800">
                            Upload Failed
                          </h3>
                          <p className="mt-1 text-sm text-red-700">
                            {uploadResult.message}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Show Errors */}
                  {uploadResult.errors && uploadResult.errors.length > 0 && (
                    <div className="mt-3 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                      <h4 className="text-sm font-medium text-yellow-800 mb-2">
                        Errors Found:
                      </h4>
                      <ul className="space-y-1 text-sm text-yellow-700">
                        {uploadResult.errors.map((err, idx) => (
                          <li key={idx}>
                            Row {err.row}: {err.error}
                          </li>
                        ))}
                      </ul>
                      {uploadResult.additional_errors &&
                        uploadResult.additional_errors > 0 && (
                          <p className="mt-2 text-xs text-yellow-600">
                            ... and {uploadResult.additional_errors} more
                            error(s)
                          </p>
                        )}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Right Column - Instructions */}
          <div className="space-y-6">
            {/* Instructions Card */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <div className="flex items-start mb-4">
                <Info className="h-5 w-5 text-blue-600 mt-0.5" />
                <h2 className="ml-2 text-lg font-semibold text-blue-900">
                  How It Works
                </h2>
              </div>
              <ol className="space-y-3 text-sm text-blue-800">
                <li className="flex items-start">
                  <span className="font-bold mr-2">1.</span>
                  <span>Download the sample CSV file to see the format</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-2">2.</span>
                  <span>
                    Fill in your product details (title, description, price,
                    image_url)
                  </span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-2">3.</span>
                  <span>Select one or more Facebook accounts</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-2">4.</span>
                  <span>Upload your CSV file</span>
                </li>
                <li className="flex items-start">
                  <span className="font-bold mr-2">5.</span>
                  <span>
                    Each post from CSV will be created for ALL selected accounts
                  </span>
                </li>
              </ol>
            </div>

            {/* CSV Format Card */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-sm font-semibold text-gray-900 mb-3">
                📋 CSV Format Instructions
              </h3>
              <div className="space-y-3 text-sm text-gray-700">
                <div>
                  <p className="font-medium text-gray-900">Required Columns:</p>
                  <ul className="mt-1 ml-4 list-disc space-y-1">
                    <li>
                      <code className="text-xs bg-gray-100 px-1 rounded">
                        title
                      </code>{" "}
                      - Product name
                    </li>
                    <li>
                      <code className="text-xs bg-gray-100 px-1 rounded">
                        description
                      </code>{" "}
                      - Post description
                    </li>
                    <li>
                      <code className="text-xs bg-gray-100 px-1 rounded">
                        price
                      </code>{" "}
                      - Product price (numbers only)
                    </li>
                  </ul>
                </div>
                <div>
                  <p className="font-medium text-gray-900">Optional Column:</p>
                  <ul className="mt-1 ml-4 list-disc">
                    <li>
                      <code className="text-xs bg-gray-100 px-1 rounded">
                        image_url
                      </code>{" "}
                      - URL of product image
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Example Card */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-sm font-semibold text-gray-900 mb-3">
                💡 Example
              </h3>
              <div className="bg-gray-50 rounded p-3 text-xs font-mono overflow-x-auto">
                <div className="whitespace-nowrap">
                  title,description,price,image_url
                </div>
                <div className="whitespace-nowrap text-gray-600">
                  iPhone 13,Like new...,699.99,https://...
                </div>
              </div>
              <p className="mt-3 text-xs text-gray-600">
                If you select 3 accounts and upload a CSV with 5 posts,
                you&apos;ll create 15 posts total (5 × 3).
              </p>
            </div>

            {/* Important Notes */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-yellow-900 mb-2">
                ⚠️ Important Notes
              </h3>
              <ul className="space-y-2 text-xs text-yellow-800">
                <li>• All posts are auto-scheduled to current time</li>
                <li>• Image URLs must be publicly accessible</li>
                <li>• Price must be a valid number (e.g., 99.99)</li>
                <li>• Posts without images are allowed</li>
                <li>• Maximum recommended: 100 rows per CSV</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

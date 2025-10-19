"use client";

import { useEffect, useState } from "react";
import { accountsAPI } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import {
  Users,
  CheckCircle,
  XCircle,
  Trash2,
  Plus,
  Upload,
  RefreshCw,
} from "lucide-react";
import AddAccountModal from "@/components/AddAccountModal";
import BulkUploadModal from "@/components/BulkUploadModal";

interface FacebookAccount {
  id: number;
  email: string;
  session_exists: boolean;
  created_at: string;
}

export default function AccountsPage() {
  const [accounts, setAccounts] = useState<FacebookAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isBulkUploadOpen, setIsBulkUploadOpen] = useState(false);
  const [updatingSessionId, setUpdatingSessionId] = useState<number | null>(
    null
  );
  const [selectedAccounts, setSelectedAccounts] = useState<number[]>([]);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    try {
      setLoading(true);
      const response = await accountsAPI.list();
      setAccounts(response.data);
    } catch (err) {
      setError("Failed to load accounts");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this account?")) return;

    try {
      await accountsAPI.delete(id);
      setAccounts(accounts.filter((acc) => acc.id !== id));
    } catch (err) {
      alert("Failed to delete account");
      console.error(err);
    }
  };

  const handleBulkDelete = async () => {
    if (selectedAccounts.length === 0) return;

    if (
      !confirm(
        `Are you sure you want to delete ${selectedAccounts.length} account(s)?`
      )
    ) {
      return;
    }

    try {
      setIsDeleting(true);
      const deletePromises = selectedAccounts.map((id) =>
        accountsAPI.delete(id)
      );
      const results = await Promise.allSettled(deletePromises);

      const successCount = results.filter(
        (r) => r.status === "fulfilled"
      ).length;
      const failCount = results.filter((r) => r.status === "rejected").length;

      if (successCount > 0) {
        alert(`Successfully deleted ${successCount} account(s)`);
        setSelectedAccounts([]);
        fetchAccounts();
      }

      if (failCount > 0) {
        alert(`Failed to delete ${failCount} account(s)`);
      }
    } catch (err) {
      alert("Failed to delete accounts");
      console.error(err);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleSelectAll = () => {
    if (selectedAccounts.length === accounts.length) {
      setSelectedAccounts([]);
    } else {
      setSelectedAccounts(accounts.map((acc) => acc.id));
    }
  };

  const handleSelectAccount = (id: number) => {
    setSelectedAccounts((prev) =>
      prev.includes(id) ? prev.filter((accId) => accId !== id) : [...prev, id]
    );
  };

  const handleUpdateSession = async (id: number) => {
    try {
      setUpdatingSessionId(id);
      const response = await accountsAPI.updateSession(id);
      alert(
        response.data.message ||
          "Browser opening for login. Please complete the login process."
      );
      // Refresh accounts after a delay to allow session update
      setTimeout(() => {
        fetchAccounts();
        setUpdatingSessionId(null);
      }, 3000);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { error?: string } } };
      alert(
        error.response?.data?.error ||
          "Failed to update session. Please try again."
      );
      setUpdatingSessionId(null);
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading accounts...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Add Account Modal */}
      <AddAccountModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={fetchAccounts}
      />

      {/* Bulk Upload Modal */}
      <BulkUploadModal
        isOpen={isBulkUploadOpen}
        onClose={() => setIsBulkUploadOpen(false)}
        onSuccess={fetchAccounts}
      />

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Facebook Accounts
          </h1>
          <p className="text-gray-600 mt-1">
            Manage your Facebook accounts for marketplace automation
          </p>
        </div>
        <div className="flex gap-3">
          <Button
            onClick={() => setIsBulkUploadOpen(true)}
            variant="purple"
            className="flex items-center gap-2"
          >
            <Upload size={20} />
            Upload Multiple Accounts
          </Button>
          <Button
            onClick={() => setIsModalOpen(true)}
            className="flex items-center gap-2"
          >
            <Plus size={20} />
            Add Account
          </Button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Total Accounts
            </CardTitle>
            <Users className="h-5 w-5 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{accounts.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              Active Sessions
            </CardTitle>
            <CheckCircle className="h-5 w-5 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">
              {accounts.filter((acc) => acc.session_exists).length}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              No Session
            </CardTitle>
            <XCircle className="h-5 w-5 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">
              {accounts.filter((acc) => !acc.session_exists).length}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Accounts Table */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex flex-col gap-2">
              <CardTitle>All Accounts</CardTitle>
              {accounts.length > 0 && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleSelectAll}
                  className="w-fit"
                >
                  {selectedAccounts.length === accounts.length
                    ? "Deselect All"
                    : "Select All"}
                </Button>
              )}
            </div>

            {/* Bulk Actions - Right Side */}
            {selectedAccounts.length > 0 && (
              <div className="flex items-center gap-3">
                <span className="text-sm font-medium text-gray-700">
                  {selectedAccounts.length} selected
                </span>
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={handleBulkDelete}
                  disabled={isDeleting}
                >
                  {isDeleting ? (
                    <>
                      <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                      Deleting...
                    </>
                  ) : (
                    <>
                      <Trash2 className="mr-2 h-4 w-4" />
                      Delete {selectedAccounts.length}
                    </>
                  )}
                </Button>
              </div>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {accounts.length === 0 ? (
            <div className="text-center py-12">
              <Users className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-semibold text-gray-900">
                No accounts
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Get started by adding a Facebook account.
              </p>
              <div className="mt-6">
                <Button>
                  <Plus size={20} className="mr-2" />
                  Add Account
                </Button>
              </div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-12">
                      {/* Checkbox column header - empty for safety */}
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Email
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Session Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Created At
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {accounts.map((account) => (
                    <tr
                      key={account.id}
                      className={`hover:bg-gray-50 ${
                        selectedAccounts.includes(account.id)
                          ? "bg-blue-50"
                          : ""
                      }`}
                    >
                      <td className="px-6 py-4 whitespace-nowrap">
                        <input
                          type="checkbox"
                          checked={selectedAccounts.includes(account.id)}
                          onChange={() => handleSelectAccount(account.id)}
                          className="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-2 focus:ring-blue-500 cursor-pointer"
                          aria-label={`Select account ${account.email}`}
                        />
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="flex-shrink-0 h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                            <Users className="h-5 w-5 text-blue-600" />
                          </div>
                          <div className="ml-4">
                            <div className="text-sm font-medium text-gray-900">
                              {account.email}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {account.session_exists ? (
                          <span className="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            <CheckCircle className="h-4 w-4 mr-1" />
                            Active
                          </span>
                        ) : (
                          <span className="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                            <XCircle className="h-4 w-4 mr-1" />
                            No Session
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(account.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <div className="flex items-center justify-end gap-2">
                          {!account.session_exists && (
                            <Button
                              variant="default"
                              size="sm"
                              onClick={() => handleUpdateSession(account.id)}
                              disabled={updatingSessionId === account.id}
                              className="flex items-center gap-1"
                            >
                              <RefreshCw
                                size={16}
                                className={
                                  updatingSessionId === account.id
                                    ? "animate-spin"
                                    : ""
                                }
                              />
                              {updatingSessionId === account.id
                                ? "Updating..."
                                : "Update Session"}
                            </Button>
                          )}
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => handleDelete(account.id)}
                            className="flex items-center gap-1"
                          >
                            <Trash2 size={16} />
                            Delete
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

"use client";

import { useState, useEffect } from "react";
import { Button } from "./ui/Button";
import { X, Upload, Calendar } from "lucide-react";
import { postsAPI, accountsAPI } from "@/lib/api";
import Image from "next/image";

interface CreatePostModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  onToast?: (type: "success" | "error", message: string) => void;
}

interface FacebookAccount {
  id: number;
  email: string;
  session_exists: boolean;
}

export default function CreatePostModal({
  isOpen,
  onClose,
  onSuccess,
  onToast,
}: CreatePostModalProps) {
  const [accounts, setAccounts] = useState<FacebookAccount[]>([]);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    price: "",
    account: "",
    scheduled_time: "",
  });
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isOpen) {
      fetchAccounts();
      // Set default scheduled time to current time
      const now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      setFormData((prev) => ({
        ...prev,
        scheduled_time: now.toISOString().slice(0, 16),
      }));
    }
  }, [isOpen]);

  const fetchAccounts = async () => {
    try {
      const response = await accountsAPI.list();
      setAccounts(response.data);
    } catch (err) {
      console.error("Failed to fetch accounts:", err);
    }
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError("Image size must be less than 5MB");
        return;
      }

      // Validate file type
      if (!file.type.startsWith("image/")) {
        setError("Please select an image file");
        return;
      }

      setImage(file);
      setError("");

      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // Validation
    if (!formData.title.trim()) {
      setError("Title is required");
      return;
    }
    if (!formData.description.trim()) {
      setError("Description is required");
      return;
    }
    if (!formData.price || parseFloat(formData.price) <= 0) {
      setError("Please enter a valid price");
      return;
    }
    if (!formData.account) {
      setError("Please select an account");
      return;
    }
    if (!image) {
      setError("Please upload an image");
      return;
    }
    if (!formData.scheduled_time) {
      setError("Please select a scheduled time");
      return;
    }

    setLoading(true);

    try {
      // Create FormData for file upload
      const submitData = new FormData();
      submitData.append("title", formData.title);
      submitData.append("description", formData.description);
      submitData.append("price", formData.price);
      submitData.append("account", formData.account);
      submitData.append("scheduled_time", formData.scheduled_time);
      if (image) {
        submitData.append("image", image);
      }

      await postsAPI.create(submitData);

      // Show success message
      if (onToast) {
        onToast("success", "Post created successfully!");
      }

      // Reset form
      setFormData({
        title: "",
        description: "",
        price: "",
        account: "",
        scheduled_time: "",
      });
      setImage(null);
      setImagePreview("");

      onSuccess();
      onClose();
    } catch (err) {
      const error = err as { response?: { data?: { error?: string } } };
      const errorMessage =
        error.response?.data?.error ||
        "Failed to create post. Please try again.";
      setError(errorMessage);

      if (onToast) {
        onToast("error", errorMessage);
      }
      console.error("Error creating post:", err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-2xl font-bold text-gray-900">
            Create Marketplace Post
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Close modal"
          >
            <X size={24} />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6">
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          <div className="space-y-4">
            {/* Account Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Facebook Account <span className="text-red-500">*</span>
              </label>
              <select
                name="account"
                value={formData.account}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                aria-label="Select Facebook account"
                required
              >
                <option value="">Select an account</option>
                {accounts.map((account) => (
                  <option key={account.id} value={account.id}>
                    {account.email}
                    {account.session_exists ? " ✓" : " (No Session)"}
                  </option>
                ))}
              </select>
              {accounts.length === 0 && (
                <p className="mt-1 text-sm text-gray-500">
                  No accounts available. Please add an account first.
                </p>
              )}
            </div>

            {/* Title */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Title <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                placeholder="e.g., iPhone 13 Pro - 256GB"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                maxLength={255}
                required
              />
              <p className="mt-1 text-sm text-gray-500">
                {formData.title.length}/255 characters
              </p>
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description <span className="text-red-500">*</span>
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                placeholder="Describe your item in detail..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={4}
                required
              />
              <p className="mt-1 text-sm text-gray-500">
                {formData.description.length} characters
              </p>
            </div>

            {/* Price */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Price ($) <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="price"
                value={formData.price}
                onChange={handleInputChange}
                placeholder="0.00"
                step="0.01"
                min="0.01"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            {/* Image Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Product Image <span className="text-red-500">*</span>
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors">
                {imagePreview ? (
                  <div className="space-y-4">
                    <Image
                      src={imagePreview}
                      alt="Preview"
                      width={400}
                      height={300}
                      className="max-h-64 mx-auto rounded-lg object-contain"
                    />
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        setImage(null);
                        setImagePreview("");
                      }}
                    >
                      Remove Image
                    </Button>
                  </div>
                ) : (
                  <div>
                    <Upload className="mx-auto h-12 w-12 text-gray-400" />
                    <p className="mt-2 text-sm text-gray-600">
                      Click to upload or drag and drop
                    </p>
                    <p className="mt-1 text-xs text-gray-500">
                      PNG, JPG, GIF up to 5MB
                    </p>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageChange}
                      className="hidden"
                      id="image-upload"
                      aria-label="Upload product image"
                    />
                    <label htmlFor="image-upload">
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        className="mt-4"
                        onClick={() =>
                          document.getElementById("image-upload")?.click()
                        }
                      >
                        Select Image
                      </Button>
                    </label>
                  </div>
                )}
              </div>
            </div>

            {/* Scheduled Time */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="inline h-4 w-4 mr-1" />
                Scheduled Time <span className="text-red-500">*</span>
              </label>
              <input
                type="datetime-local"
                name="scheduled_time"
                value={formData.scheduled_time}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
              <p className="mt-1 text-sm text-gray-500">
                When should this post be published to Facebook?
              </p>
            </div>
          </div>

          {/* Footer */}
          <div className="flex gap-3 mt-6 pt-6 border-t">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              disabled={loading}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={loading || accounts.length === 0}
              className="flex-1"
            >
              {loading ? "Creating..." : "Create Post"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

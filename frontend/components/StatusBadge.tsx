"use client";

import React from "react";

interface StatusBadgeProps {
  status: "pending" | "posting" | "posted" | "failed";
  errorMessage?: string;
}

export default function StatusBadge({
  status,
  errorMessage,
}: StatusBadgeProps) {
  const getStatusStyles = () => {
    switch (status) {
      case "pending":
        return {
          bg: "bg-yellow-100",
          text: "text-yellow-800",
          icon: "⏳",
          label: "Pending",
        };
      case "posting":
        return {
          bg: "bg-blue-100",
          text: "text-blue-800",
          icon: "🔄",
          label: "Posting...",
        };
      case "posted":
        return {
          bg: "bg-green-100",
          text: "text-green-800",
          icon: "✅",
          label: "Posted",
        };
      case "failed":
        return {
          bg: "bg-red-100",
          text: "text-red-800",
          icon: "❌",
          label: "Failed",
        };
      default:
        return {
          bg: "bg-gray-100",
          text: "text-gray-800",
          icon: "❓",
          label: "Unknown",
        };
    }
  };

  const { bg, text, icon, label } = getStatusStyles();

  return (
    <div className="inline-flex items-center gap-1">
      <span
        className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium ${bg} ${text}`}
        title={errorMessage || label}
      >
        <span>{icon}</span>
        <span>{label}</span>
      </span>
      {status === "failed" && errorMessage && (
        <span className="text-red-600 text-xs cursor-help" title={errorMessage}>
          ℹ️
        </span>
      )}
    </div>
  );
}

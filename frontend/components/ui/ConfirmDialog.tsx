"use client";

import React from "react";
import { Button } from "./Button";
import { AlertTriangle, CheckCircle, Trash2, Send } from "lucide-react";

interface ConfirmDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
  type?: "danger" | "warning" | "success" | "info";
  confirmText?: string;
  cancelText?: string;
  icon?: React.ReactNode;
}

export default function ConfirmDialog({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  type = "warning",
  confirmText = "OK",
  cancelText = "Cancel",
  icon,
}: ConfirmDialogProps) {
  if (!isOpen) return null;

  const handleConfirm = () => {
    onConfirm();
    onClose();
  };

  const getTypeStyles = () => {
    switch (type) {
      case "danger":
        return {
          bg: "bg-red-50",
          iconColor: "text-red-600",
          confirmBtn: "bg-red-600 hover:bg-red-700",
          borderColor: "border-red-200",
          defaultIcon: <Trash2 className="h-12 w-12" />,
        };
      case "warning":
        return {
          bg: "bg-yellow-50",
          iconColor: "text-yellow-600",
          confirmBtn: "bg-yellow-600 hover:bg-yellow-700",
          borderColor: "border-yellow-200",
          defaultIcon: <AlertTriangle className="h-12 w-12" />,
        };
      case "success":
        return {
          bg: "bg-green-50",
          iconColor: "text-green-600",
          confirmBtn: "bg-green-600 hover:bg-green-700",
          borderColor: "border-green-200",
          defaultIcon: <CheckCircle className="h-12 w-12" />,
        };
      case "info":
        return {
          bg: "bg-blue-50",
          iconColor: "text-blue-600",
          confirmBtn: "bg-blue-600 hover:bg-blue-700",
          borderColor: "border-blue-200",
          defaultIcon: <Send className="h-12 w-12" />,
        };
    }
  };

  const styles = getTypeStyles();

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-md mx-4 animate-in fade-in zoom-in duration-200">
        {/* Icon Section */}
        <div
          className={`${styles.bg} ${styles.borderColor} border-b px-6 pt-8 pb-6 rounded-t-xl`}
        >
          <div className={`${styles.iconColor} flex justify-center mb-4`}>
            {icon || styles.defaultIcon}
          </div>
          <h3 className="text-xl font-bold text-gray-900 text-center">
            {title}
          </h3>
        </div>

        {/* Message Section */}
        <div className="px-6 py-6">
          <p className="text-gray-600 text-center leading-relaxed">{message}</p>
        </div>

        {/* Action Buttons */}
        <div className="px-6 pb-6 flex gap-3">
          <Button onClick={onClose} variant="outline" className="flex-1 h-11">
            {cancelText}
          </Button>
          <Button
            onClick={handleConfirm}
            className={`flex-1 h-11 text-white ${styles.confirmBtn}`}
          >
            {confirmText}
          </Button>
        </div>
      </div>
    </div>
  );
}

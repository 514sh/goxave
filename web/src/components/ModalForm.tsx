import React, { useState } from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (value: string) => void;
  modalType: "informational" | "success" | "error";
}

export const ModalForm: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  modalType,
}) => {
  const [inputValue, setInputValue] = useState("");

  if (!isOpen) return null;

  // Determine modal classes and header text based on modalType
  const modalStyles = {
    informational: {
      className:
        "w-11/12 max-w-md rounded-lg border bg-white border-gray-300 shadow-lg sm:w-full p-6",
      headerText: "Input Form",
    },
    success: {
      className:
        "w-11/12 max-w-md rounded-lg border bg-green-50 border-green-500 shadow-lg sm:w-full p-6",
      headerText: "Input Form (Success)",
    },
    error: {
      className:
        "w-11/12 max-w-md rounded-lg border bg-red-50 border-red-500 shadow-lg sm:w-full p-6",
      headerText: "Input Form (Error)",
    },
  };

  const { className, headerText } =
    modalStyles[modalType] || modalStyles.informational;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSubmit(inputValue.trim());
      setInputValue("");
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
    >
      <div className={className}>
        {/* Header with close button */}
        <div className="mb-4 flex items-center justify-between">
          <div className="text-foreground font-serif text-lg">{headerText}</div>
          <button
            aria-label="Close"
            onClick={onClose}
            className="text-foreground hover:text-red focus:text-red transition-colors"
            type="button"
          >
            &#x2715;
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              required
              placeholder="Enter your discord server webhook"
              className="border-border text-foreground w-full rounded border bg-white p-2 font-sans focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
          </div>

          {/* Buttons */}
          <div className="flex justify-end space-x-3">
            <button
              onClick={onClose}
              type="button"
              className="bg-secondary hover:bg-red focus:bg-aqua text-foreground rounded px-4 py-2 font-semibold transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="bg-primary hover:bg-aqua focus:bg-aqua text-foreground rounded px-4 py-2 font-semibold transition-colors"
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ModalForm;

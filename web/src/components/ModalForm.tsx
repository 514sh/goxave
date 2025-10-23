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
        "w-11/12 max-w-md rounded-lg border bg-surface border-gray-300 shadow-lg sm:w-full p-6",
      headerText: "Add/Edit your discord webhook",
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

  const handleOnSkip = (event: React.FormEvent) => {
    event.preventDefault();
    localStorage.setItem("showModalDiscordWebhook", "SKIPPED");
    setInputValue("");
    onClose();
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
            className="text-foreground hover:text-red focus:text-red rounded-full transition-colors"
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
              placeholder="Enter your discord server webhook"
              className="border-border text-foreground bg-surface focus:ring-aqua w-full rounded border p-2 font-sans focus:ring-2 focus:outline-none"
            />
          </div>

          {/* Buttons */}
          <div className="flex justify-end space-x-3">
            <button
              onClick={handleOnSkip}
              type="button"
              className="bg-secondary hover:bg-aqua focus:bg-aqua text-foreground rounded px-4 py-2 font-semibold transition-colors hover:text-white"
            >
              Skip
            </button>
            <button
              type="submit"
              className="bg-primary hover:bg-aqua focus:bg-aqua text-foreground rounded px-4 py-2 font-semibold transition-colors hover:text-white"
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

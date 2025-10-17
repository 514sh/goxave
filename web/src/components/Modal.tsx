import React from "react";

interface ModalProps {
  message: string;
  modalType: "informational" | "success" | "error";
  isOpen: boolean;
  onClose: () => void;
}

export const Modal: React.FC<ModalProps> = ({
  message,
  modalType,
  isOpen,
  onClose,
}) => {
  if (!isOpen) return null;

  // Determine modal classes and header text based on modalType
  const modalStyles = {
    informational: {
      className:
        "w-11/12 max-w-md rounded-lg border bg-white border-gray-300 shadow-lg sm:w-full p-6",
      headerText: "Notice",
    },
    success: {
      className:
        "w-11/12 max-w-md rounded-lg border bg-green-50 border-green-500 shadow-lg sm:w-full p-6",
      headerText: "Success",
    },
    error: {
      className:
        "w-11/12 max-w-md rounded-lg border bg-red-50 border-red-500 shadow-lg sm:w-full p-6",
      headerText: "Error",
    },
  };

  const { className, headerText } =
    modalStyles[modalType] || modalStyles.informational;

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

        {/* Message */}
        <div className="mb-6 text-gray-900">{message}</div>

        {/* Buttons */}
        <div className="flex justify-end space-x-3">
          <button
            onClick={onClose}
            className="bg-primary hover:bg-aqua hover:text-foreground rounded px-4 py-2 font-semibold text-white transition-colors"
            type="button"
          >
            OK
          </button>
        </div>
      </div>
    </div>
  );
};

export default Modal;

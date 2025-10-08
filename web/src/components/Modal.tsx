import React from "react";

interface ModalProps {
  message: string;
  isOpen: boolean;
  onClose: () => void;
}

export const Modal: React.FC<ModalProps> = ({ message, isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div
      className="w-11/12 max-w-md rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-6 shadow-lg sm:w-full"
      role="dialog"
      aria-modal="true"
    >
      {/* Header with close button */}
      <div className="mb-4 flex items-center justify-between">
        <div className="text-lg font-semibold text-[var(--color-foreground)]">
          Notice
        </div>
        <button
          aria-label="Close"
          onClick={onClose}
          className="text-[var(--color-muted)] transition hover:text-[var(--color-red)]"
          type="button"
        >
          &#x2715;
        </button>
      </div>

      {/* Message */}
      <div className="mb-6 text-[var(--color-foreground)]">{message}</div>

      {/* Buttons */}
      <div className="flex justify-end space-x-3">
        <button
          onClick={onClose}
          className="rounded bg-[var(--color-muted)] px-4 py-2 font-semibold text-white transition hover:bg-[var(--color-orange)]"
          type="button"
        >
          OK
        </button>
      </div>
    </div>
  );
};

export default Modal;

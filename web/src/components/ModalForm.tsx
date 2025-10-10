import React, { useState } from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (value: string) => void;
}

export const ModalForm: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
}) => {
  const [inputValue, setInputValue] = useState("");

  if (!isOpen) return null;

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
      className="w-11/12 max-w-md rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-6 shadow-lg sm:w-full"
      role="dialog"
      aria-modal="true"
    >
      <div className="mb-4 flex items-center justify-between">
        <div className="text-lg font-semibold text-[var(--color-foreground)]">
          Input Form
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

      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            required
            placeholder="Enter required value"
            className="w-full rounded border border-[var(--color-border)] bg-[var(--color-background)] p-2 text-[var(--color-foreground)]"
          />
        </div>

        <div className="flex justify-end space-x-3">
          <button
            onClick={onClose}
            type="button"
            className="rounded bg-[var(--color-muted)] px-4 py-2 font-semibold text-white transition hover:bg-[var(--color-orange)]"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="rounded bg-[var(--color-primary)] px-4 py-2 font-semibold text-white transition hover:bg-[var(--color-primary-hover)]"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  );
};

export default ModalForm;

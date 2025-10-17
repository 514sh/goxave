import React from "react";

const Loading: React.FC = () => {
  return (
    <div
      className="bg-surface/80 fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm"
      role="status"
      aria-live="polite"
      aria-label="Loading content, please wait"
    >
      <div className="flex flex-col items-center gap-4">
        {/* Spinner */}
        <div
          className="border-foreground/20 border-t-foreground h-12 w-12 animate-spin rounded-full border-4 border-t-4"
          aria-hidden="true"
        ></div>
        {/* Loading Text */}
        <span className="text-foreground text-lg font-medium">Loading...</span>
      </div>
    </div>
  );
};

export default Loading;

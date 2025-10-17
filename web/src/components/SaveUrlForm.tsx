import React, { useState } from "react";

import productService from "../services/products";
import type { MessageType } from "../types";
import Modal from "./Modal";

const SaveUrlForm = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [message, setMessage] = useState<string>("");
  const [messageType, setMessageType] = useState<MessageType>("informational");
  const handleSaveUrl = async (event: React.FormEvent) => {
    event.preventDefault();
    console.log("clicked");
    const response = await productService.addNew(url);
    if (!response) return;
    setIsOpen(true);
    setMessage(response.message);
    setMessageType(response.type);
    console.log(response);
  };

  const onClose = () => {
    setIsOpen(false);
  };

  const handleChangeUrl = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(event.target.value);
  };
  const [url, setUrl] = useState<string>("");
  if (isOpen)
    return (
      <div className="flex-items-center flex justify-center">
        <Modal
          modalType={messageType}
          isOpen={isOpen}
          message={message}
          onClose={onClose}
        />
      </div>
    );
  return (
    <div className="flex-items-center flex justify-center">
      <form
        className="flex basis-[66dvw] flex-col items-center gap-6 rounded-lg p-6 shadow-md"
        onSubmit={handleSaveUrl}
      >
        <input
          className="placeholder-muted border-border w-full rounded-md border px-4 py-2"
          placeholder="Paste url here"
          onChange={handleChangeUrl}
        />

        <button className="border-border hover:bg-orange bg-primary text-bold active:bg-orange focus:bg-orange rounded-md border px-4 py-2 font-serif text-white transition focus:text-white active:text-white">
          Save
        </button>
      </form>
    </div>
  );
};

export default SaveUrlForm;

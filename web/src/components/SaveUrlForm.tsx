import React, { useState } from "react";

import { stores } from "../constants";
import productService from "../services/products";
import type { MessageType } from "../types";
import Modal from "./Modal";

const SaveUrlForm = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [message, setMessage] = useState<string>("");
  const [messageType, setMessageType] = useState<MessageType>("informational");
  const [showStores, setShowStores] = useState<boolean>(false);
  const [url, setUrl] = useState<string>("");

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

  const toggleStores = () => {
    setShowStores(!showStores);
  };

  const closeStores = () => {
    setShowStores(false);
  };

  if (isOpen)
    return (
      <div className="flex items-center justify-center">
        <Modal
          modalType={messageType}
          isOpen={isOpen}
          message={message}
          onOk={onClose}
          onClose={onClose}
        />
      </div>
    );

  return (
    <div className="bg-surface text-foreground flex min-h-screen flex-col items-center justify-start pt-8 font-sans sm:pt-4">
      <form
        className="flex w-full max-w-[66vw] flex-col items-center gap-6 rounded-lg p-6 shadow-md sm:max-w-[90vw]"
        onSubmit={handleSaveUrl}
      >
        <input
          className="placeholder-muted border-border w-full rounded-md border px-4 py-2 text-base sm:text-sm"
          placeholder="Paste URL here"
          onChange={handleChangeUrl}
        />
        <button className="border-border hover:bg-orange bg-primary text-bold active:bg-orange focus:bg-orange rounded-md border px-4 py-2 font-serif text-base text-white transition focus:text-white active:text-white sm:text-sm">
          Save
        </button>
        <div className="text-center font-sans text-sm sm:text-sm">
          <p>
            Track item prices by adding a URL.{" "}
            <span
              className="text-aqua hover:text-purple cursor-pointer underline"
              onClick={toggleStores}
            >
              View
            </span>{" "}
            supported stores.
          </p>
        </div>
      </form>
      {showStores && (
        <div className="mt-4 flex w-full max-w-[66vw] items-center justify-center sm:max-w-[90vw]">
          <div className="relative w-full rounded-lg p-6 shadow-md">
            <button
              className="text-foreground hover:text-red absolute top-2 right-2 text-lg sm:text-base"
              onClick={closeStores}
            >
              ✕
            </button>
            <div className="overflow-x-auto">
              <table className="w-full table-auto">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="px-4 py-2 text-left text-base sm:text-sm">
                      Logo
                    </th>
                    <th className="px-4 py-2 text-left text-base sm:text-sm">
                      Store
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {stores.map((store) => (
                    <tr key={store.id} className="border-b border-gray-100">
                      <td className="px-4 py-2">
                        <img
                          src={store.logo}
                          alt={`${store.name} logo`}
                          className="h-8 w-8 object-contain sm:h-6 sm:w-6"
                        />
                      </td>
                      <td className="px-4 py-2">
                        <a
                          href={store.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-aqua hover:text-purple text-base sm:text-sm"
                        >
                          {store.name}
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SaveUrlForm;

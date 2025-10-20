import { useEffect, useRef, useState } from "react";
import { useLoaderData, useNavigate } from "react-router";

import productService from "../services/products";
import userService from "../services/users";
import type { ProfileLoaderData } from "../types";
import Loading from "./Loading";
import Modal from "./Modal";
import ModalForm from "./ModalForm";

const Profile = () => {
  const { savedItems, userInfo } = useLoaderData() as ProfileLoaderData;
  const [openDropdownId, setOpenDropdownId] = useState<string | null>(null);
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isOpenModalForm, setIsOpenModalForm] = useState<boolean>(false);
  const [toBeDeleted, setToBeDeleted] = useState<string | null>(null);
  const navigate = useNavigate();
  const dropdownRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const handleSubmitModalForm = (discordWebhook: string) => {
    userService.addDiscordWebhook(discordWebhook).then((response) => {
      console.log(response);
    });
    navigate("/profile", { replace: true });
  };

  const handleOpenEditWebhook = () => {
    setIsOpenModalForm(true);
  };

  const handleDelete = async (productId: string) => {
    setOpenDropdownId(null);
    setIsOpen(true);
    setToBeDeleted(productId);
  };

  const handleMoreDetails = (productId: string) => {
    setOpenDropdownId(null);
    navigate(`/profile/${productId}`);
    setIsLoading(true);
    console.log(productId);
  };

  const handleMoreInfoClick = (productId: string) => {
    // Toggle dropdown: open if closed, close if open
    setOpenDropdownId(openDropdownId === productId ? null : productId);
  };

  const onCloseModal = () => {
    setIsOpen(false);
    setToBeDeleted(null);
    setIsOpenModalForm(false);
  };

  const onOkModal = async () => {
    setIsOpen(false);
    if (toBeDeleted !== null) await productService.removeOne(toBeDeleted);
    setToBeDeleted(null);
    navigate("/profile", { replace: true });
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      // Check if click is outside both the dropdown and the button
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        buttonRef.current &&
        !buttonRef.current.contains(event.target as Node)
      ) {
        setOpenDropdownId(null);
      }
    };

    // Add event listener
    document.addEventListener("mousedown", handleClickOutside);

    // Cleanup event listener on component unmount
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  if (isLoading) return <Loading />;
  if (isOpen)
    return (
      <div className="flex-items-center flex justify-center">
        <Modal
          modalType="informational"
          isOpen={isOpen}
          message="Are you sure you want to delete this product?"
          ok="Continue"
          onOk={onOkModal}
          onClose={onCloseModal}
        />
      </div>
    );
  if (isOpenModalForm) {
    return (
      <ModalForm
        modalType={"informational"}
        isOpen={isOpenModalForm}
        onClose={onCloseModal}
        onSubmit={handleSubmitModalForm}
      />
    );
  }

  if (Array.isArray(savedItems) && savedItems.length === 0) {
    return (
      <section className="mx-auto max-w-4xl p-4 sm:p-6">
        <h2 className="mb-6 font-serif text-2xl font-semibold">Saved items</h2>
        <div className="mb-6 font-sans font-semibold">
          You have no saved items.
        </div>
      </section>
    );
  }
  return (
    <>
      <section className="mx-auto max-w-4xl p-4 sm:p-6">
        <h2 className="mb-4 font-serif text-2xl font-semibold">
          Profile Information
        </h2>
        <div className="border-border rounded-lg border p-4 shadow-sm">
          <div className="space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-muted font-sans text-sm font-medium">Name</p>
                <p className="font-sans text-base">{userInfo.name}</p>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-muted font-sans text-sm font-medium">
                  Email
                </p>
                <p className="font-sans text-base">{userInfo.email}</p>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-center">
                <div>
                  <p className="text-muted font-sans text-sm font-medium">
                    Discord Webhook
                  </p>
                  <div className="flex items-center">
                    <p className="font-sans text-base break-all">
                      {userInfo.discordWebhook}
                    </p>
                    <button
                      onClick={handleOpenEditWebhook}
                      className="hover:text-purple focus:text-purple text-aqua ml-2 text-sm font-medium underline transition-colors"
                    >
                      Edit
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section className="mx-auto max-w-4xl p-4 sm:p-6">
        <h2 className="mb-6 font-serif text-2xl font-semibold">Saved items</h2>

        <div className="space-y-4">
          {savedItems &&
            savedItems.map((myProduct) => {
              return (
                <div
                  key={myProduct.id}
                  className="border-border relative flex flex-col items-center space-y-4 rounded-lg border p-4 shadow-sm transition-shadow hover:shadow-md sm:flex-row sm:items-start sm:space-y-0 sm:space-x-4"
                >
                  {/* Vertical Ellipsis Button */}
                  <button
                    ref={buttonRef}
                    onClick={() => handleMoreInfoClick(myProduct.id)}
                    aria-label="More options for this product"
                    aria-expanded={
                      openDropdownId === myProduct.id ? "true" : "false"
                    }
                    className="hover:bg-secondary focus:secondary active:bg-secondary text-foreground absolute right-2 bottom-2 z-10 rounded px-2 py-1 text-lg font-bold transition-colors hover:text-white focus:text-white active:text-white sm:top-2 sm:right-2"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-6 w-6"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      aria-hidden="true"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={4}
                        d="M12 5v.01M12 12v.01M12 19v.01"
                      />
                    </svg>
                  </button>

                  {/* Dropdown Menu */}
                  {openDropdownId === myProduct.id && (
                    <div
                      ref={dropdownRef}
                      className="border-border absolute right-2 bottom-10 z-20 w-32 rounded-md border bg-white shadow-md sm:top-10 sm:bottom-auto sm:w-40"
                    >
                      <button
                        onClick={() => handleMoreDetails(myProduct.id)}
                        className="hover:bg-orange focus:bg-orange block w-full rounded-t-md px-3 py-2 text-left text-sm text-gray-700 transition-colors hover:text-white focus:text-white"
                      >
                        More Details
                      </button>
                      <button
                        onClick={() => handleDelete(myProduct.id)}
                        className="hover:bg-orange focus:bg-orange block w-full rounded-b-md px-3 py-2 text-left text-sm text-red-600 transition-colors hover:text-white focus:text-white"
                      >
                        Delete
                      </button>
                    </div>
                  )}

                  <img
                    src={myProduct.productImage.src}
                    alt={myProduct.productImage.alt}
                    className="h-48 w-full flex-shrink-0 rounded-md object-cover sm:h-24 sm:w-24"
                  />

                  <div className="text-center sm:text-left">
                    <a
                      href={myProduct.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:bg-secondary focus:bg-secondary active:bg-secondary block w-full rounded px-2 text-left font-serif text-lg font-bold transition-colors"
                    >
                      {myProduct.productName}
                    </a>
                    <p className="text-muted mt-1 px-2">
                      Current price: {myProduct.productPrice}
                    </p>
                  </div>
                </div>
              );
            })}
        </div>
      </section>
    </>
  );
};

export default Profile;

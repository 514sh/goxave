import { useState } from "react";

const NavBar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b-2 border-border font-serif round-md shadow-md bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex-shrink-0">
            <a href="#" className="text-xl font-bold">
              GoXave
            </a>
          </div>

          {/* Hamburger button for small screens */}
          <div className="sm:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              type="button"
              className="inline-flex items-center justify-center p-2 rounded-md hover:bg-orange hover:text-white active:bg-orange active:text-white focus:bg-orange focus:text-white"
              aria-controls="mobile-menu"
              aria-expanded={isOpen}
            >
              <svg
                className="h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                {isOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>

          {/* Desktop menu */}
          <div className="hidden sm:flex sm:space-x-8">
            <a
              href="#"
              className="hover:bg-orange hover:text-white  px-3 py-2 rounded-md"
            >
              Home
            </a>
            <a
              href="#"
              className="hover:bg-orange hover:text-white  px-3 py-2 rounded-md"
            >
              Profile
            </a>
            <a
              href="#"
              className="hover:bg-orange hover:text-white  px-3 py-2 rounded-md"
            >
              FAQ
            </a>
            <a
              href="#"
              className="hover:bg-orange hover:text-white  px-3 py-2 rounded-md"
            >
              Logout
            </a>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-surface bg-opacity-95 z-60 flex flex-col p-4 space-y-4 sm:hidden"
          id="mobile-menu"
        >
          <button
            onClick={() => setIsOpen(false)}
            className="self-end p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-white hover:bg-orange hover:text-white active:bg-orange active:text-white focus:bg-orange focus:text-white"
            aria-label="Close menu"
          >
            <svg
              className="h-6 w-6"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
          <a
            href="#"
            className="block px-3 py-2 rounded-md hover:bg-orange hover:text-white active:bg-orange active:text-white focus:bg-orange focus:text-white"
          >
            Home
          </a>
          <a
            href="#"
            className="block px-3 py-2 rounded-md hover:bg-orange hover:text-white active:bg-orange active:text-white focus:bg-orange focus:text-white"
          >
            Profile
          </a>
          <a
            href="#"
            className="block px-3 py-2 rounded-md hover:bg-orange hover:text-white active:bg-orange active:text-white focus:bg-orange focus:text-white"
          >
            FAQ
          </a>
          <a
            href="#"
            className="block px-3 py-2 rounded-md hover:bg-orange hover:text-white active:bg-orange active:text-white focus:bg-orange focus:text-white"
          >
            Logout
          </a>
        </div>
      )}
    </nav>
  );
};

export default NavBar;

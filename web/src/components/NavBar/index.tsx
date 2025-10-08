import { useState } from "react";
import { Link } from "react-router";

const NavBar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="border-border round-md bg-background fixed top-0 right-0 left-0 z-50 border-b-2 font-serif shadow-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex-shrink-0">
            <Link to="/" className="text-xl font-bold">
              GoXave
            </Link>
          </div>

          {/* Hamburger button for small screens */}
          <div className="sm:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              type="button"
              className="hover:bg-orange active:bg-orange focus:bg-orange inline-flex items-center justify-center rounded-md p-2 hover:text-white focus:text-white active:text-white"
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
            <Link
              to="/"
              className="hover:bg-orange rounded-md px-3 py-2 hover:text-white"
            >
              Home
            </Link>
            <Link
              to="/profile"
              className="hover:bg-orange rounded-md px-3 py-2 hover:text-white"
            >
              Profile
            </Link>
            <Link
              to="/FAQ"
              className="hover:bg-orange rounded-md px-3 py-2 hover:text-white"
            >
              FAQ
            </Link>
            <Link
              to="/logout"
              className="hover:bg-orange rounded-md px-3 py-2 hover:text-white"
            >
              Logout
            </Link>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div
          className="bg-surface bg-opacity-95 fixed inset-0 z-60 flex flex-col space-y-4 p-4 sm:hidden"
          id="mobile-menu"
        >
          <button
            onClick={() => setIsOpen(false)}
            className="hover:bg-orange active:bg-orange focus:bg-orange self-end rounded-md p-2 hover:text-white focus:text-white focus:ring-2 focus:ring-white focus:outline-none active:text-white"
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
          <Link
            to="/"
            className="hover:bg-orange active:bg-orange focus:bg-orange block rounded-md px-3 py-2 hover:text-white focus:text-white active:text-white"
          >
            Home
          </Link>
          <Link
            to="/profile"
            className="hover:bg-orange active:bg-orange focus:bg-orange block rounded-md px-3 py-2 hover:text-white focus:text-white active:text-white"
          >
            Profile
          </Link>
          <Link
            to="/faq"
            className="hover:bg-orange active:bg-orange focus:bg-orange block rounded-md px-3 py-2 hover:text-white focus:text-white active:text-white"
          >
            FAQ
          </Link>
          <Link
            to="/logout"
            className="hover:bg-orange active:bg-orange focus:bg-orange block rounded-md px-3 py-2 hover:text-white focus:text-white active:text-white"
          >
            Logout
          </Link>
        </div>
      )}
    </nav>
  );
};

export default NavBar;

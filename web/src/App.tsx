import { useEffect, useState } from "react";
import { Outlet, useLocation, useNavigate } from "react-router";

import ModalForm from "./components/ModalForm";
import Navbar from "./components/NavBar";
import loginService from "./services/logins";
import userService from "./services/users";

function App() {
  const navigate = useNavigate();
  const location = useLocation();
  const [showModal, setShowModal] = useState<boolean>(false);

  const closeModal = () => {
    setShowModal(false);
  };

  const handleSubmitModal = (discordWebhook: string) => {
    userService.addDiscordWebhook(discordWebhook).then((response) => {
      console.log(response);
    });
  };
  useEffect(() => {
    loginService.validateLogin().then((response) => {
      console.log("root", response);
      if (!response.isValid) {
        navigate("/login", { replace: true });
      } else if (!response.withDiscord) {
        setShowModal(!response.withDiscord);
      }
    });
  }, [navigate, location.pathname]);

  return (
    <div className="bg-surface text-foreground flex min-h-screen flex-col font-sans">
      <Navbar />
      <div className="pt-24">
        {showModal ? (
          <ModalForm
            isOpen={showModal}
            onClose={closeModal}
            onSubmit={handleSubmitModal}
          />
        ) : (
          <></>
        )}
        <Outlet />
      </div>
    </div>
  );
}

export default App;

import { useEffect } from "react";
import { Outlet, useLocation, useNavigate } from "react-router";

import Navbar from "./components/NavBar";
import loginService from "./services/logins";

function App() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    loginService.validateLogin().then((isValid) => {
      if (!isValid) {
        navigate("/login", { replace: true });
        console.log("root", isValid);
      }
    });
  }, [navigate, location.pathname]);

  return (
    <div className="bg-surface text-foreground flex min-h-screen flex-col font-sans">
      <Navbar />
      <div className="pt-24">
        <Outlet />
      </div>
    </div>
  );
}

export default App;

import { useEffect } from "react";
import { useNavigate } from "react-router";

import loginService from "../services/logins";

const SignOut = () => {
  const navigate = useNavigate();
  useEffect(() => {
    loginService.invalidateLogin();
    navigate("/login", { replace: true });
  }, [navigate]);
  return <>logging out...</>;
};
export default SignOut;

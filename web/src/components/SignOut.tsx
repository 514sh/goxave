import { useEffect } from "react";
import { useNavigate } from "react-router";

import loginService from "../services/logins";
import Loading from "./Loading";

const SignOut = () => {
  const navigate = useNavigate();
  useEffect(() => {
    loginService.invalidateLogin();
    navigate("/login", { replace: true });
  }, [navigate]);
  return <Loading />;
};
export default SignOut;

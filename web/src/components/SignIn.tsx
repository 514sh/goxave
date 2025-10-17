import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router";

import { firebaseConfig } from "../config";
import loginService from "../services/logins";
import type { AuthUserResult } from "../types";
import Loading from "./Loading";
import StyledFirebaseAuth from "./StyledFirebaseAuth";

// Initialize Firebase
initializeApp(firebaseConfig);

const SignInScreen = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const uiConfig = {
    signInFlow: "redirect",
    callbacks: {
      signInSuccessWithAuthResult: (authResult: AuthUserResult) => {
        const user = authResult.user;
        loginService.newLogin(user.accessToken).then((res) => {
          setIsLoading(false);
          if (res.valid_token) {
            const from = location.state?.from || "/";
            navigate(from, { replace: true });
          }
        });
        return false; // Prevent automatic redirect by Firebase UI
      },
    },
    signInSuccessUrl: "/", // Used with redirect flow
    signInOptions: [GoogleAuthProvider.PROVIDER_ID],
  };

  useEffect(() => {
    loginService.validateLogin().then((response) => {
      setIsLoading(false);
      if (response.isValid) {
        const from = location.state?.from || "/";
        navigate(from, { replace: true });
      }
    });
  }, [navigate, location.state?.from]);

  if (isLoading) return <Loading />;

  return (
    <div className="bg-background flex min-h-screen flex-col items-center justify-center">
      <div className="container mx-auto flex max-w-5xl flex-col items-center justify-between px-4 md:flex-row">
        <div className="mb-8 text-center md:mb-0 md:w-1/2 md:text-left">
          <h1 className="text-foreground mb-4 font-serif text-4xl font-bold md:text-5xl">
            goSave
          </h1>
          <p className="text-muted max-w-md text-lg md:text-xl">
            Track prices across your favorite online stores and get instant
            notifications when prices change. Save smarter with goSave.
          </p>
        </div>

        <div className="flex justify-center md:w-1/2 md:justify-end">
          <div className="bg-surface border-border w-full max-w-sm rounded-lg border p-6 shadow-sm">
            <StyledFirebaseAuth uiConfig={uiConfig} firebaseAuth={getAuth()} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignInScreen;

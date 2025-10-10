// Import FirebaseAuth and firebase.
// Note: https://github.com/firebase/firebaseui-web-react/pull/173
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router";

import { firebaseConfig } from "../config";
import loginService from "../services/logins";
import type { AuthUserResult } from "../types";
import StyledFirebaseAuth from "./StyledFirebaseAuth";

// Configure Firebase.
initializeApp(firebaseConfig);

const SignInScreen = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean | null>(null);

  const uiConfig = {
    // Popup signin flow rather than redirect flow.
    signInFlow: "popup",
    callbacks: {
      // This function runs after a successful sign-in.
      signInSuccessWithAuthResult: (authResult: AuthUserResult) => {
        const user = authResult.user;
        loginService.newLogin(user.accessToken).then((res) => {
          setLoading(false);
          console.log(res);
          if (res.valid_token) navigate("/", { replace: true });
        });
        return false;
      },
    },
    // Redirect to /signedIn after sign in is successful. Alternatively you can provide a callbacks.signInSuccess function.
    signInSuccessUrl: "/",
    // We will display Google and Facebook as auth providers.
    signInOptions: [GoogleAuthProvider.PROVIDER_ID],
  };

  useEffect(() => {
    loginService.validateLogin().then((response) => {
      console.log("validate login", response);
      setLoading(false);
      if (response.isValid) {
        navigate("/", { replace: true });
      }
    });
  }, [navigate]);

  if (loading === null) return <>loading...</>;

  return (
    <div>
      <StyledFirebaseAuth uiConfig={uiConfig} firebaseAuth={getAuth()} />
    </div>
  );
};

export default SignInScreen;

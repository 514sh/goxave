// Import FirebaseAuth and firebase.
// Note: https://github.com/firebase/firebaseui-web-react/pull/173
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router";

import { firebaseConfig } from "../config";
import loginService from "../services/logins";
import type { AuthUserResult } from "../types";
import Loading from "./Loading";
import StyledFirebaseAuth from "./StyledFirebaseAuth";

// Configure Firebase.
initializeApp(firebaseConfig);

const SignInScreen = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const uiConfig = {
    // Popup signin flow rather than redirect flow.
    signInFlow: "popup",
    callbacks: {
      // This function runs after a successful sign-in.
      signInSuccessWithAuthResult: (authResult: AuthUserResult) => {
        const user = authResult.user;
        loginService.newLogin(user.accessToken).then((res) => {
          setIsLoading(false);
          console.log(res);
          if (res.valid_token) {
            const from = location.state?.from || "/";
            navigate(from, { replace: true });
          }
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
      setIsLoading(false);
      if (response.isValid) {
        const from = location.state?.from || "/";
        navigate(from, { replace: true });
      }
    });
  }, [navigate, location.state?.from]);

  if (isLoading) return <Loading />;

  return (
    <div>
      <StyledFirebaseAuth uiConfig={uiConfig} firebaseAuth={getAuth()} />
    </div>
  );
};

export default SignInScreen;

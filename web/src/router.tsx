import { createBrowserRouter } from "react-router";

import App from "./App";
import FAQ from "./components/FAQ";
import Pingpong from "./components/Pingpong";
import Profile from "./components/Profile";
import SaveUrlForm from "./components/SaveUrlForm";
import SignInScreen from "./components/SignIn";
import SignOut from "./components/SignOut";

const router = createBrowserRouter([
  {
    path: "/",
    Component: App,
    children: [
      { index: true, Component: SaveUrlForm },
      { path: "profile", Component: Profile },
      { path: "ping", Component: Pingpong },
      { path: "faq", Component: FAQ },
      { path: "logout", Component: SignOut },
    ],
  },
  {
    path: "/login",
    Component: SignInScreen,
  },
]);

export default router;

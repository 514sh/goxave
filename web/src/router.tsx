import { createBrowserRouter } from "react-router";

import App from "./App";
import Profile from "./components/Profile";
import Pingpong from "./components/Pingpong";
import SaveUrlForm from "./components/SaveUrlForm";

const router = createBrowserRouter([
  {
    path: "/",
    Component: App,
    children: [
      { index: true, Component: SaveUrlForm },
      { path: "profile", Component: Profile },
      { path: "ping", Component: Pingpong },
    ],
  },
]);

export default router;

import { createBrowserRouter } from "react-router";

import App from "./App";
import Profile from "./components/Profile";
import SaveUrlForm from "./components/SaveUrlForm";

const router = createBrowserRouter([
  {
    path: "/",
    Component: App,
    children: [
      { index: true, Component: SaveUrlForm },
      { path: "profile", Component: Profile },
    ],
  },
]);

export default router;

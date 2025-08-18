import { Outlet } from "react-router";

import Navbar from "./components/NavBar";

function App() {
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

import { useEffect, useState } from "react";

import { get } from "../utils/fetch";

const Pingpong = () => {
  const url = "/api/ping";
  const [pingResult, setPingResult] = useState<string | null>(null);
  useEffect(() => {
    get(url).then((res) => setPingResult(res));
  }, []);
  if (!pingResult) {
    return <>loading...</>;
  }
  return <>{pingResult}</>;
};

export default Pingpong;

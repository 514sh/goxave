import axios from "axios";

import type { UserInfo } from "../types";
const baseUrl = "/api/users";

const addDiscordWebhook = async (discordWebhook: string) => {
  const response = await axios.post(baseUrl, {
    discord_webhook: discordWebhook,
  });
  return response.data;
};

const getUserInfo = async (): Promise<UserInfo> => {
  const response = await axios.get(baseUrl, {
    withCredentials: true,
  });
  return {
    name: response.data.name,
    email: response.data.email,
    discordWebhook: response.data.discord_webhook,
  };
};

const services = {
  addDiscordWebhook,
  getUserInfo,
};

export default services;

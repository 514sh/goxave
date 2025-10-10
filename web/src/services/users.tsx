import axios from "axios";

const baseUrl = "/api/users";

const addDiscordWebhook = async (discordWebhook: string) => {
  const response = await axios.post(baseUrl, {
    discord_webhook: discordWebhook,
  });
  return response.data;
};

const services = {
  addDiscordWebhook,
};

export default services;

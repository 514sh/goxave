import axios from "axios";

const baseUrl = "/api/login";

const newLogin = async (token: string) => {
  const headers = {
    Authorization: `Bearer ${token}`,
  };
  const response = await axios.post(baseUrl, null, {
    headers,
  });
  return response.data;
};

const validateLogin = async () => {
  try {
    const response = await axios.get(baseUrl);
    return {
      isValid: Boolean(response.data.valid_token),
      withDiscord: Boolean(response.data.with_discord),
    };
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.log(error.response);
      return {
        isValid: Boolean(error.response?.data?.valid_token),
        withDiscord: Boolean(error.response?.data?.with_discord),
      };
    }
  }
  return {
    isValid: false,
    withDiscord: false,
  };
};

const invalidateLogin = async () => {
  const response = await axios.delete(baseUrl);
  console.log("logging out", response);
  return response;
};

const services = {
  newLogin,
  validateLogin,
  invalidateLogin,
};

export default services;

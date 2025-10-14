import axios from "axios";

const baseUrl = "/api/products";

const getAll = async () => {
  try {
    const response = await axios.get(baseUrl, {
      withCredentials: true,
    });
    console.log("getall", response);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) return [];
  }
};

const addNew = async (url: string) => {
  try {
    const response = await axios.post(baseUrl, {
      url,
      withCredentials: true,
    });
    console.log("add new product", response);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) return error.response.data;
  }

  return null;
};

const services = {
  getAll,
  addNew,
};

export default services;

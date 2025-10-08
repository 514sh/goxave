import axios from "axios";

const baseUrl = "/api/products";

const getAll = async () => {
  const response = await axios.get(baseUrl);
  console.log("getall", response);
  return response.data;
};

const addNew = async (url: string) => {
  try {
    const response = await axios.post(baseUrl, {
      url,
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

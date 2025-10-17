import axios from "axios";

import type { AddNewProductResponse } from "../types";

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

const addNew = async (url: string): Promise<AddNewProductResponse | null> => {
  try {
    const response = await axios.post(baseUrl, {
      url,
      withCredentials: true,
    });
    console.log("add new product", response);
    return {
      redirect: response.data?.redirect,
      message: response.data?.message,
      type: response.data?.type,
    };
  } catch (error) {
    if (axios.isAxiosError(error) && error.response)
      return {
        redirect: error.response.data?.redirect,
        message: error.response.data?.message,
        type: error.response.data?.type,
      };
  }

  return null;
};

const services = {
  getAll,
  addNew,
};

export default services;

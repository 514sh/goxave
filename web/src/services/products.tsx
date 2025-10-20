import axios from "axios";

import type { AddNewProductResponse, Product, ProductResult } from "../types";

const baseUrl = "/api/products";

const getAll = async (): Promise<ProductResult[]> => {
  const response = await axios.get(baseUrl, {
    withCredentials: true,
  });
  return response.data.map((product: Product) => {
    return {
      id: product._id,
      url: product.url,
      productName: product.product_name,
      productPrice: product.product_price,
      priceHistory: product.price_history,
      productImage: product.product_image,
    };
  });
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

const getOne = async (productId: string): Promise<ProductResult> => {
  const response = await axios.get(`${baseUrl}/${productId}`, {
    withCredentials: true,
  });
  return {
    id: response.data._id,
    url: response.data._url,
    productName: response.data.product_name,
    productPrice: response.data.product_price,
    priceHistory: response.data.price_history,
    productImage: response.data.product_image,
  };
};

const removeOne = async (productId: string): Promise<null> => {
  const response = await axios.delete(`${baseUrl}/${productId}`, {
    withCredentials: true,
  });
  console.log(response);
  return null;
};

const services = {
  getAll,
  addNew,
  getOne,
  removeOne,
};

export default services;

export interface Product {
  product_name: string;
  product_price: string;
}

export interface ProductImage {
  src: string;
  alt: string;
}

export interface ProductResult {
  _id: string;
  url: string;
  product_name: string;
  product_price: string;
  price_history: [];
  product_image: ProductImage;
}

export interface AuthUser {
  accessToken: string;
}

export interface AuthUserResult {
  user: AuthUser;
}

export type MessageType = "informational" | "error" | "success";

export interface AddNewProductResponse {
  redirect: "/";
  message: string;
  type: MessageType;
}

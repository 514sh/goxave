export interface Product {
  _id: string;
  url: string;
  product_name: string;
  product_price: string;
  price_history: ProductHistory[];
  product_image: ProductImage;
}

export interface ProductImage {
  src: string;
  alt: string;
}

export interface ProductHistory {
  price: number;
  currency: string;
  timestamp: number;
}

export interface ProductResult {
  id: string;
  url: string;
  productName: string;
  productPrice: string;
  priceHistory: ProductHistory[];
  productImage: ProductImage;
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

export interface ProductLoaderParams {
  params: { productId?: string };
}

export interface UserInfo {
  name: string;
  email: string;
  discordWebhook: string;
}

export interface ProfileLoaderData {
  savedItems: ProductResult[];
  userInfo: UserInfo;
}

export interface LoginCredentials {
  isValid: boolean;
  withDiscord: boolean;
}

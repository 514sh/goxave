import type { LoaderFunctionArgs } from "react-router";
import { createBrowserRouter } from "react-router";

import App from "./App";
import FAQ from "./components/FAQ";
import Pingpong from "./components/Pingpong";
import ProductDetails from "./components/ProductDetails";
import Profile from "./components/Profile";
import SaveUrlForm from "./components/SaveUrlForm";
import SignInScreen from "./components/SignIn";
import SignOut from "./components/SignOut";
import productService from "./services/products";
import userService from "./services/users";
import type {
  ProductLoaderParams,
  ProductResult,
  ProfileLoaderData,
} from "./types";

const profileLoader = async (): Promise<ProfileLoaderData> => {
  const productResponse = await productService.getAll();
  const userInfo = await userService.getUserInfo();
  return { savedItems: productResponse, userInfo: userInfo };
};

const productDetailsLoader = async ({
  params,
}: LoaderFunctionArgs<ProductLoaderParams>): Promise<ProductResult | null> => {
  if (!params.productId) return null;
  const productResponse = await productService.getOne(params.productId);
  return productResponse;
};

const router = createBrowserRouter([
  {
    path: "/",
    Component: App,

    children: [
      {
        index: true,
        Component: SaveUrlForm,
      },
      {
        path: "profile",
        children: [
          {
            loader: profileLoader,
            HydrateFallback: () => [],
            index: true,
            Component: Profile,
          },
          {
            path: ":productId",
            loader: productDetailsLoader,
            Component: ProductDetails,
            HydrateFallback: () => null,
          },
        ],
      },
      { path: "ping", Component: Pingpong },
      { path: "faq", Component: FAQ },
    ],
  },
  {
    path: "/login",
    Component: SignInScreen,
  },

  { path: "/logout", Component: SignOut },
]);

export default router;

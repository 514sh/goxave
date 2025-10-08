import { useEffect, useState } from "react";

import productService from "../services/products";
import type { ProductResult } from "../types";
const Profile = () => {
  const [myProducts, setMyProducts] = useState<ProductResult[] | null>(null);
  useEffect(() => {
    productService.getAll().then((response) => setMyProducts(response));
  }, []);

  if (Array.isArray(myProducts) && myProducts.length === 0) {
    return (
      <section className="mx-auto max-w-4xl p-4 sm:p-6">
        <h2 className="mb-6 font-serif text-2xl font-semibold">Saved items</h2>
        <div className="mb-6 font-sans font-semibold">
          You have no saved items.
        </div>
      </section>
    );
  }
  return (
    <section className="mx-auto max-w-4xl p-4 sm:p-6">
      <h2 className="mb-6 font-serif text-2xl font-semibold">Saved items</h2>

      <div className="space-y-4">
        {myProducts &&
          myProducts.map((myProduct) => {
            return (
              <div
                key={myProduct._id}
                className="border-border flex flex-col items-center space-y-4 rounded-lg p-4 shadow-sm transition-shadow hover:shadow-md sm:flex-row sm:items-start sm:space-y-0 sm:space-x-4"
              >
                <img
                  src={myProduct.product_image.src}
                  alt={myProduct.product_image.alt}
                  className="h-48 w-full flex-shrink-0 rounded-md object-cover sm:h-24 sm:w-24"
                />

                <div className="text-center sm:text-left">
                  <a
                    href={myProduct.url}
                    target="_blank"
                    className="hover:bg-orange active:bg-orange focus:bg-orange w-full rounded px-2 text-left font-serif text-lg font-bold hover:text-white focus:text-white active:text-white"
                  >
                    {myProduct.product_name}
                  </a>
                  <p className="text-muted mt-1 px-2">
                    Current price: {myProduct.product_price}
                  </p>
                </div>
              </div>
            );
          })}
      </div>
    </section>
  );
};

export default Profile;

import type { Product } from "../types";

export const get = async (url: string): Promise<string | null> => {
  try {
    const response = await fetch(url, {});
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const result = await response.text();
    return result;
  } catch (error) {
    if (error instanceof Error) console.error(error.message);
    return null;
  }
};

export const post = async (
  url: URL,
  headers = {},
  body = {}
): Promise<string | Product> => {
  const response = await fetch(url, {
    method: "post",
    headers: { ...headers, "Content-type": "application/json" },
    body: JSON.stringify(body),
  });
  return await response.text();
};

export const generateUuidv4 = () => {
  return crypto.randomUUID();
};

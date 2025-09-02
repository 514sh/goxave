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

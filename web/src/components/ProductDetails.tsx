import { format } from "date-fns";
import { useMemo,useState } from "react";
import { useLoaderData, useNavigate } from "react-router";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { ProductResult } from "../types";
import Loading from "./Loading";

const ProductDetails = () => {
  const productResponse = useLoaderData() as ProductResult;
  const navigate = useNavigate(); // Added for closing functionality
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Calculate the most frequent currency and prepare chart data
  const { data, currency } = useMemo(() => {
    if (!productResponse?.priceHistory?.length) {
      return { data: [], currency: "" };
    }

    // Count currencies
    const currencies = new Map<string, number>();
    for (const product of productResponse.priceHistory) {
      const currency = product.currency;
      currencies.set(currency, (currencies.get(currency) || 0) + 1);
    }

    // Find the currency with the highest count
    const [highestCurrency] = [...currencies.entries()].reduce(
      ([maxCurrency, maxCount], [currency, count]) =>
        count > maxCount ? [currency, count] : [maxCurrency, maxCount],
      ["", 0]
    );

    // Filter and format data for the chart
    const chartData = productResponse.priceHistory
      .filter((priceInfo) => priceInfo.currency === highestCurrency)
      .map((priceInfo) => ({
        ...priceInfo,
        dateStr: format(new Date(priceInfo.timestamp), "MMM dd, yyyy"),
      }));

    return { data: chartData, currency: highestCurrency };
  }, [productResponse]);

  // Handle close button click
  const handleClose = () => {
    navigate(-1); // Go back to the previous page
    setIsLoading(true);
  };
  if (isLoading) return <Loading />;

  // Handle empty or invalid data
  if (!productResponse?.priceHistory?.length || !data.length) {
    return (
      <div className="relative flex min-h-[200px] items-center justify-center rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4 font-[var(--font-sans)] text-[var(--color-foreground)]">
        <p>
          No price history data available for{" "}
          {productResponse?.productName || "this product"}.
        </p>
        <button
          onClick={handleClose}
          className="absolute top-2 right-2 rounded-full p-2 text-[var(--color-foreground)] transition-colors hover:bg-[var(--color-border)]"
          aria-label="Close"
        >
          <svg
            className="h-5 w-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl p-4 sm:p-6">
      <div className="relative rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4 shadow-sm sm:p-6">
        <button
          onClick={handleClose}
          className="absolute top-2 right-2 rounded-full p-2 text-[var(--color-foreground)] transition-colors hover:bg-[var(--color-border)]"
          aria-label="Close"
        >
          <svg
            className="h-5 w-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
        <h2 className="mb-4 font-serif text-lg font-bold text-[var(--color-foreground)] sm:text-xl">
          Price History for {productResponse.productName}
        </h2>
        <div className="w-full">
          <ResponsiveContainer width="100%" aspect={1.618} minHeight={300}>
            <LineChart
              data={data}
              margin={{ top: 10, right: 20, bottom: 10, left: 10 }}
              aria-label={`Price history chart for ${productResponse.productName} in ${currency}`}
            >
              <CartesianGrid
                stroke="var(--color-border)"
                strokeDasharray="5 5"
              />
              <XAxis
                dataKey="dateStr"
                tick={{ fill: "var(--color-foreground)", fontSize: "0.875rem" }}
                tickMargin={10}
                fontFamily="var(--font-sans)"
              />
              <YAxis
                tick={{ fill: "var(--color-foreground)", fontSize: "0.875rem" }}
                fontFamily="var(--font-sans)"
                width={60}
                label={{
                  value: `Price in ${currency}`,
                  position: "insideLeft",
                  angle: -90,
                  fill: "var(--color-foreground)",
                  fontSize: "0.875rem",
                  fontFamily: "var(--font-sans)",
                }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "var(--color-surface)",
                  border: "1px solid var(--color-border)",
                  color: "var(--color-foreground)",
                  fontFamily: "var(--font-sans)",
                }}
              />
              <Line
                type="monotone"
                dataKey="price"
                stroke="var(--color-aqua)"
                strokeWidth={2}
                name={`Price in ${currency}`}
                dot={{ r: 3, fill: "var(--color-aqua)" }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default ProductDetails;

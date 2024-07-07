// frontend/src/app/[symbol]/components/fetchStockData.tsx
"use client";
import { fetchStockBySymbol } from "@/lib/utils";
import { useEffect, useState } from "react";
import { FetchStockDataResult } from "./types";

const useFetchStockData = (symbol: string): FetchStockDataResult => {
  const [stock, setStock] = useState<any>(null);
  const [relatedTickers, setRelatedTickers] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  console.log("Fetching Stock Data:", symbol, "...");

  useEffect(() => {
    const fetchData = async () => {
      if (symbol && typeof symbol === "string") {
        try {
          const stockData = await fetchStockBySymbol(symbol);
          setStock(stockData);

          if (stockData.related_tickers) {
            try {
              const tickers = JSON.parse(stockData.related_tickers);
              console.log("Parsed Related Tickers:", tickers); // Verify parsed JSON
              setRelatedTickers(tickers);
            } catch (error) {
              console.error("Error parsing Related Tickers JSON:", error);
              setRelatedTickers([]);
            }
          } else {
            console.error("No Related Tickers found for:", symbol);
            setRelatedTickers([]);
          }
        } catch (error) {
          console.error("Error fetching stock:", error);
        } finally {
          setLoading(false);
        }
      } else {
        console.error("No symbol provided in URL");
        setLoading(false);
      }
    };

    fetchData();
  }, [symbol]);

  return { stock, relatedTickers, loading };
};

export default useFetchStockData;
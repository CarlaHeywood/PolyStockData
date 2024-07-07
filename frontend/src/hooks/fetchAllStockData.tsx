// frontend/src/app/[symbol]/components/fetchStockData.tsx
"use client";
import { fetchStocks } from "@/lib/utils";
import { useEffect, useState } from "react";
import { FetchStockDataResult } from "./types";

const useFetchAllStockData = () => {
  const [stocks, setStocks] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchStockData = async () => {
      try {
        const allStockData = await fetchStocks();
        setStocks(allStockData);
      } catch (error) {
        console.error("Error fetching all stocks:", error);
      } finally {
          setLoading(false);
      }
    };

    fetchStockData();
  }, []);

  return { stocks, loading };
};

export default useFetchAllStockData;
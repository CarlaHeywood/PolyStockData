// src/app/dashboard/page.tsx
"use client";
import React, { Suspense } from "react";
import { formatDate } from "@/lib/utils";
import { Card } from "@/components/ui/card";
import { ChevronLeft, CircleAlert, Star } from "lucide-react";
import { useRouter } from "next/navigation";
import Loader from "../../components/loading";
import useFetchAllStockData from "@/hooks/fetchAllStockData";
import StocksTable from "@/components/stocks-table";
import { Alert } from "@/components/ui/alert";


const Dashboard = () => {
  const { stocks, loading } = useFetchAllStockData();
  const router = useRouter();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen w-screen">
        <Loader />
      </div>
    );
  }

  if (stocks.length === 0) {
    return (
      <div className="flex items-center justify-center p-10">
        <Alert className="color-red-700 bg-red-100" variant="destructive">
          <div className="flex flex-cols gap-5 ">
            <CircleAlert />
            <div className="flex w-auto">No stocks found</div>
          </div>
        </Alert>
      </div>
    );
  }

  return (
    <div className="p-3 lg:py-3 lg:container space-y-3">
      <Card className="rounded-full">
        <div className="flex flex-cols p-5 justify-between align-middle items-center w-full">
          <div className="flex items-center justify-start">
            <button onClick={() => router.back()}>
              <ChevronLeft />
            </button>
          </div>
          <div className="flex items-center justify-center">
            {stocks.length > 1 ? formatDate(stocks[1].previous_date) : ""}
          </div>
          <div className="flex items-center justify-end">
            <Star />
          </div>
        </div>
      </Card>
      <Card className="flex flex-wrap lg:flex-nowrap space-y-3 lg:space-x-3">
        <Suspense fallback={<Loader />}>
          <StocksTable stocks={stocks} />
        </Suspense>
      </Card>
    </div>
  );
};

export default Dashboard;

// src/app/[stock.symbol]/page.tsx
"use client";
import React from "react";
import { truncateString } from "@/lib/utils";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card } from "@/components/ui/card";
import { ArrowUpRight, ChevronLeft, CircleAlert, Star } from "lucide-react";
import { useParams, useRouter } from "next/navigation";
import TradingViewWidget from "@/components/chart"
import StockIcon from "@/components/stock-logo-icon";
import Marquee from "react-fast-marquee";
import Loader from "../../components/loading";
import fetchStockData from "@/hooks/fetchStockData";
import { Alert } from "@/components/ui/alert";


const StockDetail = () => {
  const router = useRouter();
  const { symbol } = useParams() as { symbol: string };

  console.log("Fetching Stock Data:", symbol);

  const { stock, relatedTickers, loading } = fetchStockData(symbol);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen w-screen">
        <Loader />
      </div>
    );
  }

  if (!stock) {
    console.log("Stock found: ", stock)
    return (
      <div className="flex items-center justify-center p-10">
        <Alert className="color-red-700 bg-red-100" variant="destructive">
          <div className="flex flex-cols gap-5 ">
            <CircleAlert />
            <div className="flex w-auto">Stock not found</div>
          </div>
        </Alert>
      </div>
    );
  }
  
  return (
    <div className="p-3 lg:py-3 lg:container space-y-3">
      <Card className="rounded-full">
        <div className="flex flex-cols justify-between p-5 align-middle items-center w-full">
          <div className="flex items-center justify-start">
            <button onClick={() => router.back()}>
              <ChevronLeft />
            </button>
          </div>
          <div className="flex items-center justify-center font-bold">
            {stock.stock_name} ({stock.symbol})
          </div>
          <div className="flex items-center justify-end">
            <Star />
          </div>
        </div>
      </Card>
      <div className="flex flex-wrap lg:flex-nowrap space-y-3 lg:space-x-3">
        <Card className="flex rounded-xl justify-center items-center align-middle w-ful lg:w-1/3">
          <div className="max-w-sm mx-auto bg-white rounded-xl overflow-hidden">
            <div className="flex flex-wrap items-center justify-center p-3 text-center">
              <StockIcon stock={stock} height={150} width={150} />
              <div className="mt-4">
                <div className="uppercase tracking-wide text-sm font-semibold">
                  {stock.stock_name}
                </div>
                <div className="mt-2 text-lg leading-tight font-medium text-black">
                  ${stock.closep}{" "}
                  <ArrowUpRight className="inline text-green-500" />
                </div>
                <p className="mt-2 text-left text-gray-500">
                  {" "}
                  {truncateString(stock.description, 150)}
                </p>
              </div>
            </div>
          </div>
        </Card>
        <Card className="p-2 w-full lg:w-2/3 h-[450px]">
          <TradingViewWidget symbol={stock.symbol} />
        </Card>
      </div>
      {/* <Card className="rounded-full">
        <div className="flex flex-cols justify-between p-2 align-middle items-center w-full">
          <h2 className="mx-5 font-bold">Key Data</h2>
        </div>
      </Card>
      <Card className="rounded-lg">
        <div className="flex flex-cols justify-between p-5 align-middle items-center w-full">
          <Table className="w-1/4">
            <TableBody>
              <TableRow className="flex flex-cols">
                <TableCell className="w-1/2 font-bold">Dividends</TableCell>
                <TableCell className="w-1/2 flex items-center justify-end font-medium">
                  INV001
                </TableCell>
              </TableRow>
              <TableRow className="flex flex-cols">
                <TableCell className="w-1/2 font-bold">Dividends</TableCell>
                <TableCell className="w-1/2 flex items-center justify-end font-medium">
                  INV001
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </Card>
      <Card className="rounded-full">
        <div className="flex flex-cols justify-between p-2 align-middle items-center w-full">
          <h2 className="mx-5 font-bold">Key Data</h2>
        </div>
      </Card>
      <Card className="rounded-lg">
        <div className="flex flex-cols justify-between p-5 align-middle items-center w-full">
          <Table className="w-1/3">
            <TableHeader>
              <TableRow>
                <TableHead className="w-[100px]">Invoice</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Method</TableHead>
                <TableHead className="text-right">Amount</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell className="font-medium">INV001</TableCell>
                <TableCell>Paid</TableCell>
                <TableCell>Credit Card</TableCell>
                <TableCell className="text-right">$250.00</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </Card> */}
      {/* Related Ticker */}
      {relatedTickers[0] !== "No Related Tickers" &&
      relatedTickers.length > 0 ? (
        <Card className="flex rounded-xlg">
          <div className="flex flex-cols justify-between py-3 align-middle items-center w-full">
            <h2 className="mx-5 w-auto">Related Tickers</h2>
            <Marquee pauseOnHover>
              {relatedTickers.map((ticker, index) => (
                <Card key={index} className="mx-2 px-5 py-2">
                  {ticker}
                </Card>
              ))}
            </Marquee>
          </div>
        </Card>
      ) : null}
    </div>
  );
};

export default StockDetail;


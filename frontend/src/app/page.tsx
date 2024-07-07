// frontend/src/app/page.tsx  Homepage
'use client';
import Loader from "@/components/loading";
import { Alert } from "@/components/ui/alert";
import useFetchAllStockData from "@/hooks/fetchAllStockData";
import { getRandomSample } from "@/lib/utils";
import { CircleAlert } from "lucide-react";
import Link from "next/link";
import React from "react";

const Home: React.FC = () => {
  const { stocks, loading } = useFetchAllStockData();
  const randomStocks = getRandomSample(stocks, 3);

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
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="min-h-max flex flex-col">
        <div className="mx-6 md:mx-12 my-6 flex flex-col md:flex-row">
          <div className="md:w-1/4 bg-white p-6 text-black rounded-lg shadow-md mb-6 md:mb-0">
            <h6 className="text-black text-sm font-semibold uppercase">
              WHAT WE DO
            </h6>
            <h2 className="text-black text-2xl font-bold my-4">
              Generate passive income identifying the best investment in your
              watchlist.
            </h2>
            <hr className="border-black border-t-2 my-4" />
            <ul className="space-y-2 text-black">
              <li>
                <Link href="/" passHref>
                  Home
                </Link>
              </li>
              <li>
                <Link href="/dashboard" passHref>
                  Dashboard
                </Link>
              </li>
              <li>
                <Link href="/profile" passHref>
                  Profile
                </Link>
              </li>
              <li>
                <Link href="/stockdetails/AAPL" passHref>
                  Example: Apple Inc.
                </Link>
              </li>
              <li>
                <Link href="/loadpolygondata" passHref>
                  {/* <a
                    data-bs-toggle="tooltip"
                    data-bs-placement="bottom"
                    data-bs-title="Delete all stocks in database and fetch most recent details from Polygon API. This will take several minutes. Only needed once a day"
                    className="hover:underline"
                  > */}
                  Update Database
                  {/* </a> */}
                </Link>
              </li>
            </ul>
          </div>
          <div className="md:w-3/4 ml-0 md:ml-12">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {randomStocks.map((stock) => (
                <div
                  key={stock.symbol}
                  className="bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-lg p-6 shadow-md"
                >
                  <strong className="text-white text-2xl font-bold">
                    <Link
                      className="hover:underline text-white"
                      href={`/${stock.symbol}`}
                    >
                      {stock.symbol}
                    </Link>
                  </strong>
                  <table className="table-auto w-full mt-4 text-white">
                    <tbody>
                      <tr>
                        <td className="font-semibold">Previous Close</td>
                        <td>{stock.closep}</td>
                      </tr>
                      <tr>
                        <td className="font-semibold">Previous Date</td>
                        <td>{stock.previous_date}</td>
                      </tr>
                      <tr>
                        <td className="font-semibold">Dividend($)</td>
                        <td>{stock.cash_amount}</td>
                      </tr>
                      <tr>
                        <td className="font-semibold">Dividend Freq.</td>
                        <td>{stock.divfrequency}</td>
                      </tr>
                      <tr>
                        <td className="font-semibold">Dividend Payout</td>
                        <td>{stock.pay_date}</td>
                      </tr>
                      <tr>
                        <td className="font-semibold">Dividends Decl.</td>
                        <td>{stock.declaration_date}</td>
                      </tr>
                      <tr>
                        <td className="font-semibold">Prev. Dividend</td>
                        <td>{stock.ex_dividend_date}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
export default Home;
import React from "react";
import { Table, TableBody, TableRow, TableCell, TableHeader, TableHead } from "@/components/ui/table";
import {
  calculateInvestmentForDividends,
  calculateInvestmentForThousandDividend,
  calculateYearsToDouble,
  calculatePercentage,
} from "@/lib/utils";
import StockIcon from "@/components/stock-logo-icon";
import { truncateString, formatNumberWithCommas } from "@/lib/utils";
import { Stock } from "@/hooks/types";

const StocksTable = ({ stocks }: { stocks: Stock[] }) => {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Symbol/Name</TableHead>
          <TableHead className="text-center">Close Price</TableHead>
          <TableHead className="text-center">Div & Yield</TableHead>
          <TableHead className="text-center w-64">
            Investment Needed for Dividends to Buy 1 Share
          </TableHead>
          <TableHead className="text-center w-48">
            Investment Needed for $1000 Dividend
          </TableHead>
          <TableHead className="text-center">Years to Double</TableHead>
          <TableHead className="text-center w-40">Dividend Frequency</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {stocks.map((stock) => {
          const { investmentNeeded, sharesNeeded } =
            calculateInvestmentForDividends(stock.closep, stock.cash_amount);
          const {
            investmentNeeded: investmentForThousand,
            sharesNeeded: sharesForThousand,
          } = calculateInvestmentForThousandDividend(
            stock.cash_amount,
            stock.closep
          );

          return (
            <TableRow key={stock.symbol}>
              <TableCell className="font-medium">
                <a href={`/${stock.symbol}`}>
                  <div className="flex items-center text-left justify-start gap-3">
                    <StockIcon stock={stock} height={48} width={48} />
                    <div>
                      <strong>{truncateString(stock.stock_name, 15)}</strong>
                      <br />
                      {stock.symbol}
                    </div>
                  </div>
                </a>
              </TableCell>
              <TableCell className="text-center">
                ${formatNumberWithCommas(stock.closep)}
              </TableCell>
              <TableCell className="text-center">
                ${stock.cash_amount} (
                {calculatePercentage(stock.cash_amount, stock.closep)}%)
              </TableCell>
              <TableCell className="text-center">
                ${investmentNeeded} ({sharesNeeded})
              </TableCell>
              <TableCell className="text-center">
                ${investmentForThousand} ({sharesForThousand})
              </TableCell>
              <TableCell className="text-center">
                ~ {calculateYearsToDouble(stock)} yrs
              </TableCell>
              <TableCell className="text-center">
                {stock.divfrequency}
              </TableCell>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
};

export default StocksTable;

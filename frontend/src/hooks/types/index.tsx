// src/hooks/types/index.tsx

export interface Stock {
  id: number;
  symbol: string;
  stock_name: string;
  closep: number;
  brandicon: string;
  brandlogo: string;
  description: string;
  cash_amount: number;
  divfrequency: number;
  previous_date: string;
  pay_date: string;
  declaration_date: string;
  ex_dividend_date: string;
}

export interface StockIconProps {
  stock: Stock;
  height: number;
  width: number;
}

export interface FetchStockDataResult {
  stock: Stock | null;
  relatedTickers: string[];
  loading: boolean;
}



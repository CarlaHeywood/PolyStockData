import React from "react";
import Image from "next/image";
import { StockIconProps } from "@/hooks/types";

const StockIcon: React.FC<StockIconProps> = ({ stock, height, width }) => {
  return (
    <>
      {stock.brandicon !== "No Icon Available" ? (
        <Image
          className="rounded-full"
          height={height}
          width={width}
          src={stock.brandicon}
          alt="Icon"
        />
      ) : stock.brandlogo !== "No Logo Available" ? (
        <Image
          className="rounded-full"
          height={height}
          width={width}
          src={stock.brandlogo}
          alt="Logo"
        />
      ) : (
        <div
          className={`rounded-full bg-current h-[${height}px] w-[${width}px]`}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width={width}
            height={height}
            viewBox={`0 0 ${height} ${width}`}
            fill="none"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="lucide lucide-line-chart"
          >
            <path d="M3 3v18h18" />
            <path d="m19 9-5 5-4-4-3 3" />
          </svg>
        </div>
      )}
    </>
  );
};

export default StockIcon;

// components/loading.tsx

"use client";
import React from "react";
import CircularProgress from "@mui/material/CircularProgress";

const Loader: React.FC = () => {
  return (
    <div>
      <CircularProgress />
    </div>
  );
};

export default Loader;

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "api.polygon.io",
        port: "",
        pathname: "/**",
      },
    ],
  },
};

export default nextConfig;

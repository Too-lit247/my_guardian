/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  env: {
    //NEXT_PUBLIC_BACKEND_URL: "http://localhost:8000/api",
    NEXT_PUBLIC_BACKEND_URL: "https://my-guardian-plus.onrender.com/api",
    //https://my-guardian-plus.onrender.com
  },
};

export default nextConfig;

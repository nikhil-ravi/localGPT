/** @type {import('next').NextConfig} */
const nextConfig = {
    rewrites: async () => {
        return [
            {
                source: "/api/:path*",
                destination:
                    process.env.NODE_ENV === "development"
                        ? `${process.env.NEXT_PUBLIC_FASTAPI_URL}/api/:path*`
                        : "/api/",
            },
            {
                source: "/docs",
                destination:
                    process.env.NODE_ENV === "development"
                        ? `${process.env.NEXT_PUBLIC_FASTAPI_URL}/docs`
                        : "/api/docs",
            },
            {
                source: "/health",
                destination:
                    process.env.NODE_ENV === "development"
                        ? `${process.env.NEXT_PUBLIC_FASTAPI_URL}/health`
                        : "/api/health",
            },
            {
                source: "/openapi.json",
                destination:
                    process.env.NODE_ENV === "development"
                        ? `${process.env.NEXT_PUBLIC_FASTAPI_URL}/openapi.json`
                        : "/api/openapi.json",
            },
        ];
    },
}

module.exports = nextConfig

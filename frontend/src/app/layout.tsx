import Appbar from "./components/Appbar";
import Providers from "./components/Providers";
import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Search Engine",
  description:
    "Search Engine on Shopee apply full text search, semantic search and image search.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <Appbar />

          {children}
        </Providers>
      </body>
    </html>
  );
}

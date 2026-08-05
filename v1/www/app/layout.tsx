import type { Metadata } from "next"
import { Geist_Mono, Inter } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"

import "./globals.css"
import { ThemeProvider } from "@/components/theme-provider"
import { cn } from "@/lib/utils"

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" })

export const metadata: Metadata = {
  title: "11brands snapshots",
  description:
    "Explorer for 11brands snapshots: every active brand, archived candidate and integration run, as captured.",
  // Brand assets from snapshot 20260805-232207 (brands/11brands), copied
  // unmodified — regenerate via the 11brands scripts, never edit or resample.
  icons: {
    icon: [
      { url: "/static/favicon-16x16.png", sizes: "16x16", type: "image/png" },
      { url: "/static/favicon-32x32.png", sizes: "32x32", type: "image/png" },
      { url: "/static/icon-192.png", sizes: "192x192", type: "image/png" },
      { url: "/static/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: "/static/apple-touch-icon.png",
  },
  openGraph: {
    title: "11brands snapshots",
    description:
      "Explorer for 11brands snapshots: every active brand, archived candidate and integration run, as captured.",
    images: [{ url: "/static/11brands-og-web.png", width: 1200, height: 630 }],
  },
}

const fontMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
})

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={cn(
        "antialiased",
        fontMono.variable,
        "font-sans",
        inter.variable
      )}
    >
      <body>
        <ThemeProvider>{children}</ThemeProvider>
        <Analytics />
      </body>
    </html>
  )
}

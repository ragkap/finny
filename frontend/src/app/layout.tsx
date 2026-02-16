import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Finny — Learn Finance, Have Fun!",
  description: "Financial literacy app for kids and teens, powered by Smartkarma",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen font-sans">{children}</body>
    </html>
  );
}

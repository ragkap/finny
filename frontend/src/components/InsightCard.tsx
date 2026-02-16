"use client";

import type { InsightCard as InsightCardType } from "@/lib/types";
import StockChart from "./StockChart";

interface InsightCardProps {
  card: InsightCardType;
}

function formatMarketCap(val: number | null | undefined): string {
  if (!val) return "--";
  if (val >= 1_000_000) return `$${(val / 1_000_000).toFixed(1)}T`;
  if (val >= 1_000) return `$${(val / 1_000).toFixed(1)}B`;
  return `$${val.toFixed(0)}M`;
}

export default function InsightCard({ card }: InsightCardProps) {
  const q = card.quote;

  // Fallback to plain text card if no structured quote
  if (!q) {
    return (
      <div className="my-2 overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm dark:border-gray-600 dark:bg-gray-800">
        <div className="px-4 py-3">
          <h3 className="font-semibold text-finny-dark dark:text-gray-100">{card.title}</h3>
          {card.text && <p className="mt-1 text-sm text-gray-700 dark:text-gray-300">{card.text}</p>}
        </div>
      </div>
    );
  }

  const changeVal = parseFloat(q.day_change_percent) || 0;
  const isPositive = changeVal >= 0;

  return (
    <div className="my-3 overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-md dark:border-gray-700 dark:bg-gray-800">
      {/* Header */}
      <div className="flex items-center justify-between px-5 pt-4 pb-2">
        <div>
          <h3 className="text-lg font-bold text-finny-dark dark:text-gray-100">
            {q.company || card.title}
          </h3>
          <span className="text-xs text-gray-400">{q.exchange}{card.ticker ? ` · ${card.ticker}` : ""}</span>
        </div>
        {q.url && (
          <a
            href={q.url}
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-lg bg-finny-primary/10 px-3 py-1 text-xs font-medium text-finny-primary transition hover:bg-finny-primary/20 dark:bg-finny-primary/20"
          >
            Research
          </a>
        )}
      </div>

      {/* Price + Change */}
      <div className="flex items-end gap-3 px-5 pb-3">
        <span className="text-3xl font-bold text-finny-dark dark:text-gray-50">
          {q.currency} {q.price}
        </span>
        <span
          className={`mb-1 flex items-center gap-1 rounded-full px-2.5 py-0.5 text-sm font-semibold ${
            isPositive
              ? "bg-finny-success/10 text-finny-success"
              : "bg-finny-warning/10 text-finny-warning"
          }`}
        >
          {isPositive ? "▲" : "▼"} {isPositive ? "+" : ""}{q.day_change_percent}%
        </span>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-4 gap-px border-t border-gray-100 bg-gray-100 dark:border-gray-700 dark:bg-gray-700">
        {[
          { label: "Market Cap", value: formatMarketCap(q.market_cap_usd) },
          { label: "P/E Ratio", value: q.pe ? q.pe.toFixed(1) : "--" },
          { label: "Div Yield", value: q.dividend_yield ? `${q.dividend_yield.toFixed(2)}%` : "--" },
          { label: "P/B Ratio", value: q.pb ? q.pb.toFixed(1) : "--" },
        ].map((stat) => (
          <div
            key={stat.label}
            className="bg-white px-3 py-2.5 text-center dark:bg-gray-800"
          >
            <div className="text-[10px] font-medium uppercase tracking-wider text-gray-400 dark:text-gray-500">
              {stat.label}
            </div>
            <div className="mt-0.5 text-sm font-semibold text-finny-dark dark:text-gray-200">
              {stat.value}
            </div>
          </div>
        ))}
      </div>

      {/* Chart */}
      {card.chart_data && card.ticker && (
        <div className="px-4 pb-3 pt-1">
          <StockChart data={card.chart_data} ticker={card.ticker} />
        </div>
      )}
    </div>
  );
}

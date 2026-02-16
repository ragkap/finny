"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface StockChartProps {
  data: { date: string; close: number }[];
  ticker: string;
}

export default function StockChart({ data, ticker }: StockChartProps) {
  if (!data || data.length === 0) return null;

  const isPositive = data[data.length - 1].close >= data[0].close;
  const color = isPositive ? "#00B894" : "#E17055";

  return (
    <div className="mt-3 h-40 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data}>
          <defs>
            <linearGradient id={`gradient-${ticker}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={color} stopOpacity={0.3} />
              <stop offset="95%" stopColor={color} stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 10 }}
            tickFormatter={(d) => d.slice(5)}
          />
          <YAxis
            tick={{ fontSize: 10 }}
            domain={["dataMin", "dataMax"]}
            tickFormatter={(v) => `$${v}`}
          />
          <Tooltip
            formatter={(value: number) => [`$${value.toFixed(2)}`, "Price"]}
            labelFormatter={(label) => `Date: ${label}`}
          />
          <Area
            type="monotone"
            dataKey="close"
            stroke={color}
            strokeWidth={2}
            fill={`url(#gradient-${ticker})`}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

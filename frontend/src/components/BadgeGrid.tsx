"use client";

import type { Badge } from "@/lib/types";

interface BadgeGridProps {
  badges: Badge[];
}

export default function BadgeGrid({ badges }: BadgeGridProps) {
  if (badges.length === 0) return null;

  return (
    <div className="rounded-xl bg-white p-4 shadow-sm dark:bg-gray-700">
      <h3 className="mb-3 text-sm font-medium text-gray-500 dark:text-gray-300">Badges</h3>
      <div className="grid grid-cols-3 gap-2">
        {badges.map((badge) => (
          <div
            key={badge.slug}
            className={`flex flex-col items-center rounded-lg p-2 text-center transition ${
              badge.earned
                ? "bg-finny-accent/10"
                : "bg-gray-100 opacity-40 grayscale dark:bg-gray-600"
            }`}
            title={badge.description}
          >
            <span className="mb-1 text-2xl">{badge.icon}</span>
            <span className="text-xs font-medium leading-tight">
              {badge.name}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

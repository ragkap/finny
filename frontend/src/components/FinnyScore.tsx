"use client";

import type { ScoreInfo } from "@/lib/types";

interface FinnyScoreProps {
  score: ScoreInfo | null;
  xpPopup?: number | null;
}

export default function FinnyScore({ score, xpPopup }: FinnyScoreProps) {
  if (!score) return null;

  return (
    <div className="relative rounded-xl bg-white p-4 shadow-sm dark:bg-gray-700">
      <div className="mb-2 flex items-center justify-between">
        <span className="text-sm font-medium text-gray-500 dark:text-gray-300">FinnyScore</span>
        <span className="text-lg font-bold text-finny-primary">
          {score.finny_score} XP
        </span>
      </div>

      {/* Level */}
      <div className="mb-3 flex items-center gap-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-finny-primary text-sm font-bold text-white">
          {score.level}
        </div>
        <span className="text-sm text-gray-600 dark:text-gray-300">Level {score.level}</span>
      </div>

      {/* XP Bar */}
      <div className="mb-1 h-3 w-full overflow-hidden rounded-full bg-gray-200 dark:bg-gray-600">
        <div
          className="xp-bar"
          style={{ width: `${score.progress_percent}%` }}
        />
      </div>
      <div className="mb-3 text-right text-xs text-gray-400">
        {score.finny_score % 500} / 500 to next level
      </div>

      {/* Streak */}
      <div className="flex items-center gap-2 rounded-lg bg-finny-accent/10 px-3 py-2">
        <span className="text-xl">🔥</span>
        <div>
          <div className="text-sm font-semibold">{score.current_streak}-day streak</div>
          <div className="text-xs text-gray-500">Best: {score.longest_streak} days</div>
        </div>
      </div>

      {/* XP Popup Animation */}
      {xpPopup && (
        <div className="xp-animation absolute right-4 top-0 text-lg font-bold text-finny-success">
          +{xpPopup} XP
        </div>
      )}
    </div>
  );
}

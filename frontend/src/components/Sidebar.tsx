"use client";

import type { Badge, ScoreInfo, UserProfile } from "@/lib/types";
import { signOut } from "@/lib/firebase";
import BadgeGrid from "./BadgeGrid";
import FinnyScore from "./FinnyScore";

interface SidebarProps {
  profile: UserProfile | null;
  score: ScoreInfo | null;
  badges: Badge[];
  xpPopup?: number | null;
  dark?: boolean;
  onToggleTheme?: () => void;
}

export default function Sidebar({ profile, score, badges, xpPopup, dark, onToggleTheme }: SidebarProps) {
  return (
    <aside className="flex w-72 flex-col gap-4 border-r border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-800">
      {/* Logo + Theme Toggle */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-finny-primary">Finny</h1>
          <p className="text-xs text-gray-400">Powered by Smartkarma</p>
        </div>
        {onToggleTheme && (
          <button
            onClick={onToggleTheme}
            className="rounded-lg p-2 text-lg transition hover:bg-gray-200 dark:hover:bg-gray-700"
            title={dark ? "Light mode" : "Dark mode"}
          >
            {dark ? "☀️" : "🌙"}
          </button>
        )}
      </div>

      {/* Profile */}
      {profile && (
        <div className="flex items-center gap-3 rounded-xl bg-white p-3 shadow-sm dark:bg-gray-700">
          {profile.avatar_url ? (
            <img
              src={profile.avatar_url}
              alt={profile.display_name}
              className="h-10 w-10 rounded-full"
            />
          ) : (
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-finny-primary text-white">
              {profile.display_name.charAt(0)}
            </div>
          )}
          <div className="min-w-0 flex-1">
            <div className="truncate text-sm font-semibold dark:text-gray-100">{profile.display_name}</div>
            <div className="text-xs text-gray-400">Level {profile.level}</div>
          </div>
        </div>
      )}

      <FinnyScore score={score} xpPopup={xpPopup} />
      <BadgeGrid badges={badges} />

      <div className="mt-auto">
        <button
          onClick={() => signOut()}
          className="w-full rounded-lg border border-gray-200 py-2 text-sm text-gray-500 transition hover:bg-gray-100 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700"
        >
          Sign Out
        </button>
      </div>
    </aside>
  );
}

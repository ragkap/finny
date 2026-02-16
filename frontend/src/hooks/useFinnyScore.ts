"use client";

import { useCallback, useEffect, useState } from "react";
import { getBadges, getScore } from "@/lib/api";
import type { Badge, ScoreInfo } from "@/lib/types";

export function useFinnyScore(isAuthenticated: boolean) {
  const [score, setScore] = useState<ScoreInfo | null>(null);
  const [badges, setBadges] = useState<Badge[]>([]);

  const refresh = useCallback(async () => {
    if (!isAuthenticated) return;
    try {
      const [s, b] = await Promise.all([getScore(), getBadges()]);
      setScore(s);
      setBadges(b);
    } catch {
      // API might not be ready
    }
  }, [isAuthenticated]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { score, badges, refresh };
}

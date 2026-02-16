"use client";

import { useCallback, useEffect, useState } from "react";

export function useTheme() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("finny-theme");
    if (saved === "dark" || (!saved && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
      setDark(true);
      document.documentElement.classList.add("dark");
    }
  }, []);

  const toggle = useCallback(() => {
    setDark((prev) => {
      const next = !prev;
      if (next) {
        document.documentElement.classList.add("dark");
        localStorage.setItem("finny-theme", "dark");
      } else {
        document.documentElement.classList.remove("dark");
        localStorage.setItem("finny-theme", "light");
      }
      return next;
    });
  }, []);

  return { dark, toggle };
}

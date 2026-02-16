"use client";

import { useEffect, useState } from "react";
import { getAuth, onAuthStateChanged, User } from "@/lib/firebase";
import { registerUser } from "@/lib/api";
import type { UserProfile } from "@/lib/types";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(getAuth(), async (firebaseUser) => {
      setUser(firebaseUser);
      if (firebaseUser) {
        try {
          const p = await registerUser();
          setProfile(p);
        } catch {
          // API might not be ready yet
        }
      } else {
        setProfile(null);
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  return { user, profile, setProfile, loading };
}

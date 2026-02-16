export interface UserProfile {
  id: string;
  firebase_uid: string;
  display_name: string;
  avatar_url: string | null;
  finny_score: number;
  level: number;
  current_streak: number;
  longest_streak: number;
}

export interface ScoreInfo {
  finny_score: number;
  level: number;
  current_streak: number;
  longest_streak: number;
  next_level_xp: number;
  progress_percent: number;
}

export interface Badge {
  slug: string;
  name: string;
  description: string;
  icon: string;
  earned: boolean;
  earned_at: string | null;
}

export interface QuoteData {
  company: string;
  exchange: string;
  currency: string;
  price: string;
  day_change_percent: string;
  market_cap_usd: number | null;
  pe: number | null;
  dividend_yield: number | null;
  pb: number | null;
  url: string | null;
}

export interface InsightCard {
  title: string;
  text: string;
  chart_data: { date: string; close: number; volume: number }[] | null;
  ticker: string | null;
  quote: QuoteData | null;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  insight_cards?: InsightCard[];
  xp_earned?: number;
  new_badges?: { slug: string; name: string; icon: string }[];
}

export interface ChatApiResponse {
  reply: string;
  insight_cards: InsightCard[];
  xp_earned: number;
  new_badges: { slug: string; name: string; icon: string }[];
  finny_score: number;
  level: number;
}

export interface StockQuote {
  ticker: string;
  name: string;
  price: number | null;
  change: number | null;
  change_percent: number | null;
  market_cap: number | null;
  pe_ratio: number | null;
  dividend_yield: number | null;
  sector: string | null;
  industry: string | null;
}

import { useEffect, useState } from "react";
import { getGold, getSignals, getEvents } from "../services/api";

import GoldChart from "../components/GoldChart";
import SignalCard from "../components/signal";
import EventFeed from "../components/EventFeed";
import PortfolioPanel from "../components/PortfolioPanel";

interface Signal {
  symbol: string;
  score: number;
  action: string;
}

interface Event {
  symbol: string;
  title: string;
}

export default function Dashboard() {
  const [gold, setGold] = useState([]);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [events, setEvents] = useState<Event[]>([]);

  useEffect(() => {
    // Should ideally use a component to select the time range, 
    // but for now we just fetch the last 24 hours of data
    const now = Math.floor(Date.now() / 1000);
    const oneDayAgo = now - 86400; // 24 hours in seconds
    
    getGold(oneDayAgo, now).then(res => setGold(res.data));
    getSignals().then(res => setSignals(res.data));
    getEvents().then(res => setEvents(res.data));
  }, []);

  return (
    <div style={{ padding: "20px", color: "white", background: "#111" }}>
      <h1>Gold Market Dashboard</h1>

      {/* Gold Chart */}
      <GoldChart data={gold} />

      {/* Signals */}
      <div style={{ display: "flex", gap: "10px", marginTop: "20px" }}>
        {signals.map((s, i) => (
          <SignalCard key={i} {...s} />
        ))}
      </div>

      {/* Events */}
      <EventFeed events={events} />

      {/* Portfolio */}
      <PortfolioPanel portfolio={{
        total: 12450,
        pnl: 8.2
      }} />
    </div>
  );
}

import { useEffect, useState, type SetStateAction } from "react";
import { getGold, getSignals, getEvents } from "../services/api";

import GoldChart from "../components/GoldChart";
import SignalCard from "../components/signal";
import EventFeed from "../components/EventFeed";
import PortfolioPanel from "../components/PortfolioPanel";

export default function Dashboard() {
  const [gold, setGold] = useState([]);
  const [signals, setSignals] = useState([]);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    getGold().then((res: { data: SetStateAction<never[]>; }) => setGold(res.data));
    getSignals().then((res: { data: SetStateAction<never[]>; }) => setSignals(res.data));
    getEvents().then((res: { data: SetStateAction<never[]>; }) => setEvents(res.data));
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

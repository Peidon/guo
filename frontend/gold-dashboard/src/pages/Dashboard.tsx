import { useEffect, useState } from "react";
import { getGold, getSignals } from "../services/api";

import GoldChart, { type GoldChartData } from "../components/GoldChart";
import SignalCard, { type SignalCardProps} from "../components/signal";


export default function Dashboard() {
  const [gold, setGold] = useState<GoldChartData[]>([]);
  const [signal, setSignal] = useState<SignalCardProps>();

  useEffect(() => {
    // Should ideally use a component to select the time range, 
    // but for now we just fetch the last 24 hours of data
    const now = Math.floor(Date.now() / 1000);
    const oneDayAgo = now - 86400 * 7; // 24 hours in seconds

    const stockSymbol = "ML8.AX";
    
    getGold(oneDayAgo, now).then(res => {
      // console.log('Gold data received:', res.data);
      setGold(res.data);
    });
    getSignals(stockSymbol).then(res => {setSignal(res.data);});
  }, []);

  return (
    <div style={{ padding: "20px", color: "white", background: "#171414ff" }}>
      <h1 style={{ color: "green" }}>Gold Market Dashboard</h1>

      {/* Gold Chart */}
      <GoldChart data={gold} />

      {/* Signals */}
      <div style={{ display: "flex", gap: "10px", marginTop: "20px" }}>
        {signal && <SignalCard {...signal} />}
      </div>

      {}

    </div>
  );
}

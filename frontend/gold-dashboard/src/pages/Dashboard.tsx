import { useEffect, useState } from "react";
import { getGold, getSignals, getStocks } from "../services/api";

import GoldChart, { type GoldChartData } from "../components/GoldChart";
import SignalCard, { type SignalCardProps} from "../components/signal";


export default function Dashboard() {
  const [gold, setGold] = useState<GoldChartData[]>([]);
  const [signals, setSignals] = useState<SignalCardProps[]>([]);
  const [, setStocks] = useState<string[]>([]);

  useEffect(() => {
    const now = Math.floor(Date.now() / 1000);
    const oneDayAgo = now - 86400 * 7;

    getGold(oneDayAgo, now).then(resp => {
      setGold(resp.data);
    });

    getStocks().then(resp => {
      setStocks(resp.data);
      // Fetch signals for all stocks after stocks are loaded
      Promise.all(
        resp.data.map((stock: string) => getSignals(stock).then(r => r.data))
      ).then((allSignals: SignalCardProps[]) => {
        setSignals(allSignals);
      });
    });
  }, []);

  return (
    <div style={{ padding: "20px", color: "white", background: "#171414ff" }}>
      <h1 style={{ color: "green" }}>Gold Market Dashboard</h1>

      {/* Gold Chart */}
      <GoldChart data={gold} />

      {/* Signals */}
      <div style={{ display: "flex", gap: "10px", marginTop: "20px", flexWrap: "wrap" }}>
        {signals.map((signal, idx) => (
          <SignalCard key={signal.symbol + idx} {...signal} />
        ))}
      </div>

    </div>
  );
}

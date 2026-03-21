type SignalCardProps = {
  symbol: string;
  score: number;
  action: "BUY" | "SELL" | string;
};

export default function SignalCard({ symbol, score, action }: SignalCardProps) {
  const color =
    action === "BUY" ? "green" :
    action === "SELL" ? "red" : "gray";

  return (
    <div style={{
      border: "1px solid #333",
      padding: "12px",
      borderRadius: "8px",
      width: "120px"
    }}>
      <h3>{symbol}</h3>
      <p style={{ color }}>{action}</p>
      <p>Score: {score}</p>
    </div>
  );
}
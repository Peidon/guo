export type SignalCardProps = {
  symbol: string;
  score: number;
  action: "BUY" | "SELL" | string;
};

export default function SignalCard(props: SignalCardProps) {
  const color =
    props.action === "BUY" ? "green" :
    props.action === "SELL" ? "red" : "gray";

  return (
    <div style={{
      border: "1px solid #333",
      padding: "12px",
      borderRadius: "8px",
      width: "120px"
    }}>
      <h3>{props.symbol}</h3>
      <p style={{ color }}>{props.action}</p>
      <p>Score: {props.score}</p>
    </div>
  );
}
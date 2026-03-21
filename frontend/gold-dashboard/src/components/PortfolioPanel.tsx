export interface PortfolioPanelProps {
  portfolio: {
    total: number;
    pnl: number;
  };
}

export default function PortfolioPanel({ portfolio }: PortfolioPanelProps) {
  return (
    <div>
      <h3>Portfolio</h3>
      <p>Total: ${portfolio.total}</p>
      <p>PnL: {portfolio.pnl}%</p>
    </div>
  );
}
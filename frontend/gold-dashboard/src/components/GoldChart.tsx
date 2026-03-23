import { CartesianGrid, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export type GoldChartData = {
  time: number; // timestamp
  price: number;
};

interface GoldChartProps {
  data: GoldChartData[];
}

export default function GoldChart({ data }: GoldChartProps) {

  const dailyData = data.reduce((acc, item) => {
    const date = new Date(item.time * 1000);
    const day = date.getDate().toString().padStart(2, '0');
    const month = date.toLocaleString('en-US', { month: 'short' });
    const year = date.getFullYear();
    const dayLabel = `${day}/${month}/${year}`;

    
    if (!acc[dayLabel]) {
      acc[dayLabel] = { total_price: 0, count: 0, timestamp: item.time };
    }
    acc[dayLabel].total_price += item.price;
    acc[dayLabel].count += 1;
    return acc;
  }, {} as Record<string, { total_price: number; count: number; timestamp: number }>);
  
  // Format data for Recharts - sort by timestamp and use timestamp for X-axis positioning
  const formattedData = Object.entries(dailyData)
    .map(([dateKey, { total_price, count, timestamp }]) => ({
      timestamp,
      timeLabel: dateKey,
      price: total_price / count
    }))
    .sort((a, b) => a.timestamp - b.timestamp);

  // Custom tick formatter for X-axis
  const formatXAxisTick = (timestamp: number) => {
    const date = new Date(timestamp * 1000);
    const day = date.getDate().toString().padStart(2, '0');
    const month = date.toLocaleString('en-US', { month: 'short' });
    return `${day}/${month}`;
  };

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={formattedData} margin={{ left: 20, right: 20, top: 20, bottom: 20 }}>
        <CartesianGrid stroke="#2e2e30ff" strokeDasharray="5 5" />
        <XAxis 
          dataKey="timestamp" 
          type="number"
          scale="time"
          domain={['dataMin', 'dataMax']}
          tickFormatter={formatXAxisTick}
        />
        <YAxis />
        <Tooltip 
          labelFormatter={(timestamp) => {
            const date = new Date(timestamp * 1000);
            const day = date.getDate().toString().padStart(2, '0');
            const month = date.toLocaleString('en-US', { month: 'short' });
            const year = date.getFullYear();
            return `${day}/${month}/${year}`;
          }}
        />
        <Line type="monotone" dataKey="price" stroke="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  );
}
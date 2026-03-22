import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

export type GoldChartData = {
  time: number; // timestamp
  price: number;
};

interface GoldChartProps {
  data: GoldChartData[];
}

export default function GoldChart({ data }: GoldChartProps) {
  // Format data for Recharts - convert Unix timestamp to readable time
  const formattedData = data.map(item => ({
    ...item,
    time: new Date(item.time * 1000).toLocaleTimeString()
  }));

  return (
    <LineChart width={600} height={250} data={formattedData}>
      <XAxis dataKey="time" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="price" stroke="#8884d8" />
    </LineChart>
  );
}
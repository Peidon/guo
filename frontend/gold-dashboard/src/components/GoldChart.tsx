import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

type GoldChartData = {
  time: number; // timestamp
  price: number;
};

interface GoldChartProps {
  data: GoldChartData[];
}

export default function GoldChart({ data }: GoldChartProps) {
  return (
    <LineChart width={600} height={250} data={data}>
      <XAxis dataKey="time" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="price" />
    </LineChart>
  );
}
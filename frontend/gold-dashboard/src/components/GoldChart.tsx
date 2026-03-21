import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

export default function GoldChart({ data }) {
  return (
    <LineChart width={600} height={250} data={data}>
      <XAxis dataKey="time" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="price" />
    </LineChart>
  );
}
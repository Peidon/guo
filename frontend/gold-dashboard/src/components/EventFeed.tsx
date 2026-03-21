interface Event {
  symbol: string;
  title: string;
}

interface EventFeedProps {
  events: Event[];
}

export default function EventFeed({ events }: EventFeedProps) {
  return (
    <div>
      <h3>Events</h3>
      {events.map((e, i) => (
        <div key={i} style={{ marginBottom: "8px" }}>
          <strong>{e.symbol}</strong>: {e.title}
        </div>
      ))}
    </div>
  );
}
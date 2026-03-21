import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const getGold = () => API.get("/gold");
export const getSignals = () => API.get("/signals");
export interface StockResponse {
  // Define the expected properties of the stock response here
  // Example:
  // symbol: string;
  // price: number;
}

export const getStock = (symbol: string): Promise<{ data: StockResponse }> => API.get(`/stocks/${symbol}`);
export const getEvents = () => API.get("/events");
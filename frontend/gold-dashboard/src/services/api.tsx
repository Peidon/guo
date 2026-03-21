import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const getGold = (begin: number, end: number) => API.get(`/gold?begin=${begin}&end=${end}`);
export const getSignals = () => API.get("/signals/ML8.AX");
export interface StockResponse {
  // Define the expected properties of the stock response here
  // Example:
  // symbol: string;
  // price: number;
}

export const getStock = (symbol: string): Promise<{ data: StockResponse }> => API.get(`/stocks/${symbol}`);
export const getEvents = () => API.get("/events");
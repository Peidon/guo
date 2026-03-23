import axios from "axios";

const API = axios.create({
  baseURL: "/api"
});

export const getGold = (begin: number, end: number) => API.get(`/gold?begin=${begin}&end=${end}`);
export const getSignals = (symbol: string) => API.get(`/signals/${symbol}`);
export const getStock = (symbol: string) => API.get(`/stocks/${symbol}`);
// export const getEvents = () => API.get("/events");
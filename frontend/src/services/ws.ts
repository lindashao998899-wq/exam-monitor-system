export const createProctorSocket = (onMessage: (data: any) => void) => {
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(`${protocol}://${window.location.host}/ws/proctor`);
  ws.onmessage = (event) => onMessage(JSON.parse(event.data));
  return ws;
};

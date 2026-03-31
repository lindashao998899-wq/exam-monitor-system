const wsUrlFromEnv = import.meta.env.VITE_WS_URL as string | undefined;

function inferWebsocketUrl() {
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  return `${protocol}://${window.location.host}/ws/proctor`;
}

export const createProctorSocket = (onMessage: (data: any) => void) => {
  const ws = new WebSocket(wsUrlFromEnv ?? inferWebsocketUrl());
  ws.onmessage = (event) => onMessage(JSON.parse(event.data));
  return ws;
};

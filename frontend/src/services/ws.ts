export const createProctorSocket = (onMessage: (data: any) => void) => {
  const ws = new WebSocket("ws://localhost:8000/ws/proctor");
  ws.onmessage = (event) => onMessage(JSON.parse(event.data));
  return ws;
};

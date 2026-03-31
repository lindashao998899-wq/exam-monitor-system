import { SessionState } from "../types";

export function RealtimeProctorPanel({ sessions }: { sessions: SessionState[] }) {
  return (
    <section>
      <h2>实时监考面板</h2>
      <table>
        <thead>
          <tr>
            <th>Session</th>
            <th>在线状态</th>
            <th>当前题号</th>
            <th>异常标记</th>
          </tr>
        </thead>
        <tbody>
          {sessions.map((s) => (
            <tr key={s.session_id}>
              <td>{s.session_id}</td>
              <td>{s.is_online ? "在线" : "离线"}</td>
              <td>{s.current_question_no}</td>
              <td>{s.abnormal_flag ? "⚠️" : "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

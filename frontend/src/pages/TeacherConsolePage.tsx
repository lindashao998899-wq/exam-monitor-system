import { useEffect, useState } from "react";

import { ExamManagementPanel } from "../components/ExamManagementPanel";
import { QuestionRecordsPanel } from "../components/QuestionRecordsPanel";
import { RealtimeProctorPanel } from "../components/RealtimeProctorPanel";
import { ReplayExportPanel } from "../components/ReplayExportPanel";
import { ScoreAnalysisPanel } from "../components/ScoreAnalysisPanel";
import { createProctorSocket } from "../services/ws";
import { QuestionRecord, SessionState } from "../types";

export function TeacherConsolePage() {
  const [sessions, setSessions] = useState<SessionState[]>([]);
  const [records] = useState<QuestionRecord[]>([]);

  useEffect(() => {
    const ws = createProctorSocket((message) => {
      if (message.type === "session_status") {
        const incoming = message.data as SessionState;
        setSessions((prev) => {
          const copy = [...prev];
          const idx = copy.findIndex((s) => s.session_id === incoming.session_id);
          if (idx >= 0) copy[idx] = incoming;
          else copy.push(incoming);
          return copy;
        });
      }
    });

    return () => ws.close();
  }, []);

  return (
    <main>
      <h1>A机教师控制台</h1>
      <ExamManagementPanel />
      <RealtimeProctorPanel sessions={sessions} />
      <QuestionRecordsPanel records={records} />
      <ScoreAnalysisPanel />
      <ReplayExportPanel />
    </main>
  );
}

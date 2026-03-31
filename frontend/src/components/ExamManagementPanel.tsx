import { useState } from "react";
import { api } from "../services/api";

export function ExamManagementPanel() {
  const [title, setTitle] = useState("");

  const createExam = async () => {
    if (!title.trim()) return;
    await api.post("/exams", { title });
    setTitle("");
  };

  return (
    <section>
      <h2>考试管理</h2>
      <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="考试名称" />
      <button onClick={createExam}>创建考试</button>
      <div>
        <button>开始</button>
        <button>暂停</button>
        <button>结束</button>
      </div>
    </section>
  );
}

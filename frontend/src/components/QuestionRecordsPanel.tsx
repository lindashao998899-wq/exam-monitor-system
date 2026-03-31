import { QuestionRecord } from "../types";

export function QuestionRecordsPanel({ records }: { records: QuestionRecord[] }) {
  return (
    <section>
      <h2>题目记录面板</h2>
      {records.map((r) => (
        <article key={r.questionNo}>
          <h4>第 {r.questionNo} 题</h4>
          <p>截图：{r.screenshot}</p>
          <p>学生答案：{r.studentAnswer}</p>
          <p>正确答案：{r.correctAnswer}</p>
          <p>用时：{r.elapsedSeconds}s</p>
        </article>
      ))}
    </section>
  );
}

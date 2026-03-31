import { api } from "../services/api";

export function ReplayExportPanel() {
  const exportPdf = async () => {
    await api.post("/reports/1/pdf");
  };
  const exportExcel = async () => {
    await api.post("/reports/1/excel");
  };

  return (
    <section>
      <h2>复盘导出</h2>
      <button onClick={exportPdf}>导出PDF报告</button>
      <button onClick={exportExcel}>导出Excel成绩表</button>
    </section>
  );
}

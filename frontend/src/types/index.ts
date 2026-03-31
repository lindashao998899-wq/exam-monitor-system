export interface SessionState {
  session_id: number;
  current_question_no: number;
  is_online: boolean;
  abnormal_flag: boolean;
}

export interface QuestionRecord {
  questionNo: number;
  screenshot: string;
  studentAnswer: string;
  correctAnswer: string;
  elapsedSeconds: number;
}

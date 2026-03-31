from sqlalchemy.orm import Session

from app.models.entities import Answer, Question


class ScoringEngine:
    @staticmethod
    def auto_score(db: Session, answer: Answer) -> Answer:
        question = db.query(Question).filter(Question.id == answer.question_id).first()
        if not question:
            return answer
        normalized_answer = answer.answer_text.strip().lower()
        normalized_correct = question.correct_answer.strip().lower()
        answer.is_correct = normalized_answer == normalized_correct
        answer.score = question.score if answer.is_correct else 0
        return answer

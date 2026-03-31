from app.db.base import Base
from app.db.session import engine


def run_migration() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    run_migration()
    print("[backend] 数据库迁移完成（create_all）")

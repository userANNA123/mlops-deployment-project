# src/app/models.py

from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

Base = declarative_base()


class ModelInput(Base):
    __tablename__ = "model_inputs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    payload: Mapped[str] = mapped_column(Text)

    output: Mapped["ModelOutput"] = relationship(
        back_populates="input", uselist=False
    )


class ModelOutput(Base):
    __tablename__ = "model_outputs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    input_id: Mapped[int] = mapped_column(ForeignKey("model_inputs.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    prediction: Mapped[int] = mapped_column(Integer)

    input: Mapped[ModelInput] = relationship(back_populates="output")

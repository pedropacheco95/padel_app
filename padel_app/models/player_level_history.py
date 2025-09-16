from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from padel_app.sql_db import db
from padel_app import model
from padel_app.tools.input_tools import Block, Field, Form


class PlayerLevelHistory(db.Model, model.Model):
    __tablename__ = "player_level_history"
    __table_args__ = {"extend_existing": True}

    page_title = "Player Level History"
    model_name = "player_level_history"

    id = Column(Integer, primary_key=True)

    player_id = Column(
        Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False
    )
    player = relationship("Player", back_populates="level_history")

    coach_id = Column(
        Integer, ForeignKey("coaches.id", ondelete="CASCADE"), nullable=False
    )
    coach = relationship("Coach", back_populates="player_levels")

    level_id = Column(
        Integer, ForeignKey("coach_levels.id", ondelete="CASCADE"), nullable=False
    )
    level = relationship("CoachLevel")

    assigned_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<PlayerLevelHistory {self.player.name} - {self.coach.name} = {self.level.name}>"

    def __str__(self):
        return f"{self.player.name} → {self.level.name} ({self.coach.name})"

    @property
    def name(self):
        return str(self)

    @classmethod
    def display_all_info(cls):
        searchable = {"field": "player", "label": "Player"}
        columns = [
            {"field": "player", "label": "Player"},
            {"field": "coach", "label": "Coach"},
            {"field": "level", "label": "Level"},
            {"field": "assigned_at", "label": "Assigned At"},
        ]
        return searchable, columns

    @classmethod
    def get_create_form(cls):
        def get_field(name, field_type, label=None, **kwargs):
            return Field(
                name=name,
                field_type=field_type,
                label=label or name.capitalize(),
                **kwargs,
            )

        info_block = Block(
            "info_block",
            "Player Level Assignment",
            fields=[
                get_field(
                    "player_id", "ManyToOne", label="Player", related_model="Player"
                ),
                get_field(
                    "coach_id", "ManyToOne", label="Coach", related_model="Coach"
                ),
                get_field(
                    "level_id", "ManyToOne", label="Level", related_model="CoachLevel"
                ),
                get_field("assigned_at", "DateTime", label="Assigned At"),
            ],
        )

        return Form(blocks=[info_block])

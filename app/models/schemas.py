from dataclasses import dataclass, field
from typing import List
from marshmallow import Schema, fields, validates, ValidationError


# --------------------------
# Data classes
# --------------------------

@dataclass
class MoveRequest:
    labyrinth: List[List[int]] = field(default_factory=list)
    position: List[int] = field(default_factory=list)
    goal: List[int] = field(default_factory=list)
    available_cheeses: List[List[int]] = field(default_factory=list)


@dataclass
class MoveResponse:
    next_position: List[int] = field(default_factory=list)


@dataclass
class HealthResponse:
    status: str = "ok"
    version: str = "1.0.0"


# --------------------------
# Schemas for validation
# --------------------------

class MoveRequestSchema(Schema):
    labyrinth = fields.List(fields.List(fields.Integer()), required=True)
    position = fields.List(fields.Integer(), required=True, validate=lambda x: len(x) == 2)
    goal = fields.List(fields.Integer(), required=True, validate=lambda x: len(x) == 2)
    available_cheeses = fields.List(fields.List(fields.Integer()), required=False, allow_none=True)

    @validates("labyrinth")
    def validate_labyrinth(self, value):
        if not value or not value[0]:
            raise ValidationError("Labyrinth cannot be empty")
        width = len(value[0])
        for row in value:
            if len(row) != width:
                raise ValidationError("All labyrinth rows must have the same width")
            if not all(cell in [0, 1] for cell in row):
                raise ValidationError("Labyrinth cells must be 0 (free) or 1 (wall)")

    @validates("position")
    def validate_position(self, value):
        if not all(isinstance(coord, int) and coord >= 0 for coord in value):
            raise ValidationError("Coordinates must be non-negative integers")

    @validates("goal")
    def validate_goal(self, value):
        if not all(isinstance(coord, int) and coord >= 0 for coord in value):
            raise ValidationError("Coordinates must be non-negative integers")


class MoveResponseSchema(Schema):
    next_position = fields.List(fields.Integer(), required=True)


class HealthResponseSchema(Schema):
    status = fields.String(default="ok")
    version = fields.String(required=True)

from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import StagedActivation
from distributions import gen_major, gen_gender
from typing import Tuple
import cytoolz as tlz
import uuid


class SemesterCell(Agent):
    def __init__(self, unique_id, model: Model, pos, semester):
        super().__init__(unique_id, model)
        self.pos: Tuple[int, int] = pos
        self.semester_code: str = semester


class Student(Agent):
    """An Agent Student"""

    def __init__(self, unique_id, model: Model, pos, major, gender):
        super().__init__(unique_id, model)
        self.pos: Tuple[int, int] = pos
        self.major: str = major
        self.gender: str = gender

    def get_next_semester(self) -> SemesterCell:
        x, y = self.pos
        next_pos = (x + 1, y)
        cellmates = self.model.grid.get_cell_list_contents([next_pos])
        next_semester = tlz.first(
            [cellmate for cellmate in cellmates if isinstance(cellmate, SemesterCell)]
        )

        return next_semester

    def move_to_semester(self, semester: SemesterCell):
        self.model.grid.move_agent(self, semester.pos)
        self.pos = semester.pos

    def progress(self):
        next_semester = self.get_next_semester()

        if next_semester.semester_code == "S6SEQ2":
            self.move_to_semester(next_semester)
            self.model.running = False
        else:
            self.move_to_semester(next_semester)


class KSUModel(Model):
    """A model simulating KSU student"""

    MODEL_STAGES = ["progress"]

    SEMESTERS = [
        "F1SEQ1",
        "F1SEQ2",
        "S1SEQ1",
        "S1SEQ2",
        "F2SEQ1",
        "F2SEQ2",
        "S2SEQ1",
        "S2SEQ2",
        "F3SEQ1",
        "F3SEQ2",
        "S3SEQ1",
        "S3SEQ2",
        "F4SEQ1",
        "F4SEQ2",
        "S4SEQ1",
        "S4SEQ2",
        "F5SEQ1",
        "F5SEQ2",
        "S5SEQ1",
        "S5SEQ2",
        "F6SEQ1",
        "F6SEQ2",
        "S6SEQ1",
        "S6SEQ2",
    ]

    def __init__(self, n_students, width: int, height: int):
        self.running = True
        self.n_students: int = n_students
        self.schedule = StagedActivation(self, stage_list=self.MODEL_STAGES)
        self.grid = SingleGrid(width, height, torus=False)

        # Generate Data for Agents
        self.ALL_MAJORS = gen_major(self.n_students)
        self.ALL_GENDERS = gen_gender(self.n_students)

        # Designating Each Semester
        for i in range(len(self.SEMESTERS)):
            for y in range(height):
                semester = SemesterCell(uuid.uuid4(), self, (i, y), self.SEMESTERS[i])
                self.grid.place_agent(semester, (i, y))

        # Adding Student to KSU Environment
        for i in range(self.n_students):
            major = self.ALL_MAJORS[i]
            gender = self.ALL_GENDERS[i]
            student = Student(i, self, (0, i), major, gender)

            self.schedule.add(student)
            self.grid.place_agent(student, (0, i))

    def step(self):
        self.schedule.step()

    def get_semester_status(self):
        for semester in self.SEMESTERS:
            yield semester

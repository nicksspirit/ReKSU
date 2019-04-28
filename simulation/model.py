from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from .distributions import gen_gender, gen_credit_hrs, gen_f1seq1_majors, MajorSwitch
from itertools import product, cycle
from typing import List, Deque
from collections import deque
import cytoolz as tlz
import numpy as np
import re


class Student(Agent):
    """An Agent Student"""

    def __init__(self, unique_id, model: Model, gender, activated=True):
        super().__init__(unique_id, model)

        self.majors: List[str] = []
        self.gender: str = gender
        self.sem_queue: Deque = deque()
        self.is_active: bool = activated
        self.earned_hrs: List[int] = [0]
        self.attempted_hrs: List[int] = [0]
        self.gpa: List[int] = [0]
        self._new_major = ""

    def step(self) -> None:
        match = re.search(r"(F1SEQ1)|(SEQ2)", self.model.semester)

        if match is None:
            return

        self.sem_queue.appendleft(f"{self.model.semester}_MAJOR")

        prev_semester = (
            tlz.first(self.sem_queue)
            if len(self.sem_queue) == 1
            else self.sem_queue.pop()
        )

        new_semester = f"{self.model.semester}_MAJOR"

        if new_semester != prev_semester:
            prev_major = tlz.last(self.majors)
            self._new_major = self.model.major_switcher.get_major(
                prev_semester, new_semester, prev_major
            )

    def advance(self):
        if self._new_major == "":
            return

        if not self.is_active:
            self.is_active = True

        self.majors.append(self._new_major)


class KSUModel(Model):
    """A model simulating KSU student"""

    def __init__(self, n_students, n_active: int, width: int, height: int):
        self.running = True
        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(width, height, torus=False)
        self.n_students: int = n_students
        self._semester_gen = self._gen_semester_code()
        self.semester = next(self._semester_gen)
        self.ALL_GENDERS = gen_gender(self.n_students)

        # Majors
        self.F1SEQ1_MAJORS = gen_f1seq1_majors(self.n_students)
        self.major_switcher = MajorSwitch()

        # Adding Student to KSU Environment
        for i in range(self.n_students):
            # Percentage of student agent that will be active and the rest inactive
            per_active = n_active / 100

            if np.random.binomial(1, per_active):
                student = Student(i, self, self.ALL_GENDERS[i])
                student.majors.append(self.F1SEQ1_MAJORS[i])
            else:
                student = Student(i, self, self.ALL_GENDERS[i], False)
                student.majors.append("E")

            self.schedule.add(student)
            self.grid.position_agent(student)

    def step(self):
        self.schedule.step()

        try:
            self.update_semester()
            self.update_credit_hrs()
            self.update_gpa()
        except StopIteration:
            self.running = False

    def update_semester(self) -> None:
        self.semester = next(self._semester_gen)

    def update_credit_hrs(self):
        active_students: List[Student] = [
            student for student in self.schedule.agents if student.is_active
        ]
        n_active_students = len(active_students)

        earned_hrs = [
            round(earned_hr)
            for earned_hr in gen_credit_hrs(self.semester, n_active_students)
        ]
        attempted_hrs = [
            round(attempted_hr)
            for attempted_hr in gen_credit_hrs(self.semester, n_active_students, False)
        ]

        for i, student in enumerate(active_students):
            curr_major = tlz.last(student.majors)

            # Check if earned & attempted credit hours exists for current semester
            if earned_hrs:
                new_earned_hrs = 0 if curr_major == "E" else earned_hrs[i]
                new_attempted_hrs = (
                    0 if curr_major == "E" else attempted_hrs[i]
                )
            else:
                new_earned_hrs = (
                    0 if curr_major == "E" else tlz.last(student.earned_hrs)
                )
                new_attempted_hrs = (
                    0
                    if curr_major == "E"
                    else tlz.last(student.attempted_hrs)
                )

            student.earned_hrs.append(new_earned_hrs)
            student.attempted_hrs.append(new_attempted_hrs)

    def update_gpa(self):
        active_students: List[Student] = [
            student for student in self.schedule.agents if student.is_active
        ]
        n_active_students = len(active_students)

        gpa = [
            round(earned_hr)
            for earned_hr in gen_credit_hrs(self.semester, n_active_students)
        ]

        for i, student in enumerate(active_students):
            curr_major = tlz.last(student.majors)

            # Check if gpa exists for current semester
            if gpa:
                new_gpa = 0 if curr_major == "E" else gpa[i]
            else:
                new_gpa = 0 if curr_major == "E" else tlz.last(student.gpa)

            student.gpa.append(new_gpa)

    @staticmethod
    def _gen_semester_code():
        semester_pos = [x for x in range(1, 7)]
        semester_season = product(semester_pos, ("F", "F", "S", "S"))
        seq = cycle([1, 2])

        for semester in semester_season:
            pos, season = semester
            yield f"{season}{pos}SEQ{next(seq)}"

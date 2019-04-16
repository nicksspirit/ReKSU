from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from distributions import gen_gender
from itertools import product, cycle


class Student(Agent):
    """An Agent Student"""

    def __init__(self, unique_id, model: Model, major, gender):
        super().__init__(unique_id, model)
        self.major: str = major
        self.gender: str = gender

    def step(self):
        pass

    def advance(self):
        pass


class KSUModel(Model):
    """A model simulating KSU student"""

    def __init__(self, n_students, width: int, height: int):
        self.running = True
        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(width, height, torus=False)
        self.n_students: int = n_students
        self._semester_gen = self._gen_semester_code()
        self.semester = next(self._semester_gen)

        # Generate Data for Agents
        self.ALL_GENDERS = gen_gender(self.n_students)

        # Adding Student to KSU Environment
        for i in range(self.n_students):
            student = Student(i, self, "Undeclared", self.ALL_GENDERS[i])

            self.schedule.add(student)
            self.grid.position_agent(student)

    def step(self):
        self.schedule.step()

        try:
            self.update_semester()
        except StopIteration:
            self.running = False

    def update_semester(self) -> None:
        self.semester = next(self._semester_gen)

    @staticmethod
    def _gen_semester_code():
        semester_pos = [x for x in range(1, 7)]
        semester_season = product(semester_pos, ("F", "F", "S", "S"))
        seq = cycle([1, 2])

        for semester in semester_season:
            pos, season = semester
            yield f'{season}{pos}SEQ{next(seq)}'

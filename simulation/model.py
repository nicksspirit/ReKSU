from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import StagedActivation
from distributions import gen_major, gen_gender


class Student(Agent):
    """An Agent Student"""

    def __init__(self, unique_id, model: Model, major, gender):
        super().__init__(unique_id, model)
        self.major: str = major
        self.gender: str = gender

    def semester_one(self):
        pass


class KSUModel(Model):
    """A model simulating KSU student"""

    MODEL_STAGES = ["semester_one"]

    def __init__(self, n_students, width: int, height: int):
        self.running = True
        self.n_students: int = n_students
        self.schedule = StagedActivation(self, stage_list=self.MODEL_STAGES)
        self.grid = SingleGrid(width, height, torus=False)

        # Generate Data for Agents
        self.ALL_MAJORS = gen_major(self.n_students)
        self.ALL_GENDERS = gen_gender(self.n_students)

        for i in range(self.n_students):
            major = self.ALL_MAJORS[i]
            gender = self.ALL_GENDERS[i]
            student = Student(i, self, major, gender)

            self.schedule.add(student)

            self.grid.position_agent(student, x=0, y=i)

    def step(self):
        self.schedule.step()

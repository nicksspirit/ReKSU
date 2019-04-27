from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
from .model import Student, KSUModel
from typing import Dict, Any
from colour import Color
import cytoolz as tlz

GLOBAL_OPTS = {"width": 20, "height": 20, "width_pixels": 500, "height_pixels": 500}


def set_agent_params(agent: Student) -> Dict:
    curr_major = tlz.last(agent.majors)

    base_params: Dict[str, Any] = {
        "Layer": 1,
        "Filled": "true",
        "text": agent.gender,
        "text_color": "white",
        "CurrentMajor": curr_major,
        "Majors": tuple(tlz.unique(agent.majors)),
    }

    if agent.is_active:
        color = "grey" if curr_major == "UNDECLARED" else Color(pick_for=curr_major).hex
        base_params["Earned Credit Hours"] = tlz.last(agent.earned_hrs)
        base_params["Attempted Credit Hours"] = tlz.last(agent.attempted_hrs)
        base_params["GPA"] = tlz.last(agent.gpa)
        base_params["Shape"] = "circle"
        base_params["Color"] = color
        base_params["r"] = 1
    else:
        base_params["Shape"] = "rect"
        base_params["Color"] = "grey"
        base_params["w"] = 1
        base_params["h"] = 1

    return base_params


student_slider = UserSettableParameter(
    "slider", "Number of Students", value=20, min_value=10, max_value=150, step=1
)

active_students = UserSettableParameter(
    "slider",
    "Number of Active Students",
    value=80,
    min_value=10,
    max_value=100,
    step=10,
)

model_params = {
    "n_students": student_slider,
    "n_active": active_students,
    "width": GLOBAL_OPTS["width"],
    "height": GLOBAL_OPTS["height"],
}


class SemesterElement(TextElement):
    """Display the semester code"""

    local_includes = ["./simulation/assets/js/TextModule.js"]

    def __init__(self):
        pass

    def render(self, model: KSUModel):
        return f"Semester: {model.semester}"


canvas_grid = CanvasGrid(
    set_agent_params,
    GLOBAL_OPTS["width"],
    GLOBAL_OPTS["height"],
    GLOBAL_OPTS["width_pixels"],
    GLOBAL_OPTS["height_pixels"],
)

semester_code = SemesterElement()

server: ModularServer = ModularServer(
    KSUModel, [canvas_grid, semester_code], "KSU Simulation", model_params
)

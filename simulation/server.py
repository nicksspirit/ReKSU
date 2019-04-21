from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from model import Student, ActiveStudent, InactiveStudent, KSUModel
from typing import Dict, Any
import cytoolz as tlz

GLOBAL_OPTS = {
    "n_students": 150,
    "width": 20,
    "height": 20,
    "width_pixels": 500,
    "height_pixels": 500,
}


def set_agent_params(agent: Student) -> Dict:
    base_params: Dict[str, Any] = {
        "Layer": 1,
        "text_color": "white",
        "Gender": agent.gender
    }

    if isinstance(agent, ActiveStudent):
        gender = "male" if agent.gender == "M" else "female"
        base_params["Shape"] = f"assets/images/{gender}-student.png"
        base_params["scale"] = 0.8
        base_params["Major"] = tuple(tlz.unique(agent.majors))
    if isinstance(agent, InactiveStudent):
        base_params["Filled"] = 1
        base_params["Color"] = "grey"
        base_params["Shape"] = "rect"
        base_params["w"] = 1
        base_params["h"] = 1
        base_params["Major"] = agent.majors

    return base_params


model_params = {
    "n_students": GLOBAL_OPTS["n_students"],
    "width": GLOBAL_OPTS["width"],
    "height": GLOBAL_OPTS["height"],
}


class SemesterElement(TextElement):
    """Display the semester code"""

    local_includes = ["assets/js/TextModule.js"]

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

server = ModularServer(
    KSUModel, [canvas_grid, semester_code], "KSU Simulation", model_params
)

server.port = 8521  # The default
server.launch()

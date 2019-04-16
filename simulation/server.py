from mesa.visualization.modules import CanvasGrid, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from model import Student, KSUModel
from typing import Dict, Union

GLOBAL_OPTS = {
    "n_students": 150,
    "width": 20,
    "height": 20,
    "width_pixels": 500,
    "height_pixels": 500,
}


def set_agent_params(agent: Student) -> Dict:
    base_params: Dict[str, Union[str, int, float]] = {"text_color": "white"}

    if isinstance(agent, Student):
        gender = "male" if agent.gender == "M" else "female"
        base_params["Layer"] = 1
        base_params["Shape"] = f"assets/images/{gender}-student.png"
        base_params["scale"] = 0.8
        base_params["Major"] = agent.major
        base_params["Gender"] = agent.gender

    return base_params


model_params = {
    "n_students": GLOBAL_OPTS["n_students"],
    "width": GLOBAL_OPTS["width"],
    "height": GLOBAL_OPTS["height"],
}


class SemesterElement(TextElement):
    """Display the semester"""

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

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import Student, SemesterCell, KSUModel
from typing import Dict, Union

GLOBAL_OPTS = {
    "n_students": 20,
    "width": 24,
    "height": 20,
    "width_pixels": 1000,
    "height_pixels": 1000,
}


def set_agent_params(agent: Union[Student, SemesterCell]) -> Dict:
    base_params: Dict[str, Union[str, int, float]] = {
        "text_color": "white",
    }

    if isinstance(agent, Student):
        gender = "male" if agent.gender == "M" else "female"
        base_params["Layer"] = 1
        base_params["Shape"] = f"assets/{gender}-student.png"
        base_params["scale"] = 0.8
        base_params["Major"] = agent.major
        base_params["Gender"] = agent.gender
    elif isinstance(agent, SemesterCell):
        base_params["Layer"] = 0
        base_params["Shape"] = "rect"
        base_params["w"] = 1
        base_params["h"] = 1
        base_params["Color"] = "grey"
        base_params["Filled"] = "true"
        base_params["text"] = agent.semester_code

    return base_params


model_params = {
    "n_students": GLOBAL_OPTS["n_students"],
    "width": GLOBAL_OPTS["width"],
    "height": GLOBAL_OPTS["height"],
}


grid = CanvasGrid(
    set_agent_params,
    GLOBAL_OPTS["width"],
    GLOBAL_OPTS["height"],
    GLOBAL_OPTS["width_pixels"],
    GLOBAL_OPTS["height_pixels"],
)

server = ModularServer(KSUModel, [grid], "KSU Simulation", model_params)

server.port = 8521  # The default
server.launch()

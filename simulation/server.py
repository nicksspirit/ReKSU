from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import Student, KSUModel
from typing import Dict

GLOBAL_OPTS = {
    "n_students": 10,
    "width": 12,
    "height": 10,
    "width_pixels": 500,
    "height_pixels": 500,
}


def set_agent_params(agent: Student) -> Dict:
    gender = "male" if agent.gender == "M" else "female"

    return {
        "Layer": 0,
        "Shape": f"assets/{gender}-student.png",
        "scale": 0.9,
        "Major": agent.major,
        "Gender": agent.gender,
    }


def model_params() -> Dict:
    return {
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

server = ModularServer(KSUModel, [grid], "KSU Simulation", model_params())

server.port = 8521  # The default
server.launch()

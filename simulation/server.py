from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import Student, KSUModel
from typing import Dict

GLOBAL_OPT = {
    "n_students": 10,
    "width": 10,
    "height": 10,
    "width_pixels": 500,
    "height_pixels": 500,
}


def set_agent_params(agent: Student) -> Dict:
    gender = "male" if agent.gender == "M" else "female"

    return {
        "Color": "red",
        "Filled": "true",
        "Layer": 0,
        "Shape": "circle",
        "Shape": f"assets/{gender}-student.png",
        "r": 0.5,
        "scale": 0.9,
        "Major": agent.major,
        "Gender": agent.gender,
    }


def model_params() -> Dict:
    return {
        "n_students": GLOBAL_OPT["n_students"],
        "width": GLOBAL_OPT["width"],
        "height": GLOBAL_OPT["height"],
    }


grid = CanvasGrid(
    set_agent_params,
    GLOBAL_OPT["width"],
    GLOBAL_OPT["height"],
    GLOBAL_OPT["width_pixels"],
    GLOBAL_OPT["height_pixels"],
)

server = ModularServer(KSUModel, [grid], "KSU Simulation", model_params())

server.port = 8521  # The default
server.launch()

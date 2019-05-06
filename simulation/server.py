from mesa.visualization.modules import CanvasGrid, TextElement, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer, VisualizationElement
from .model import Student, KSUModel
from typing import Dict, Any
from colour import Color
import cytoolz as tlz
import numpy as np

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
        color = "grey" if curr_major == "E" else Color(pick_for=curr_major).hex
        base_params["Earned Credit Hours"] = agent.earned_hrs
        base_params["Attempted Credit Hours"] = agent.attempted_hrs
        base_params["GPA"] = agent.gpa
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
    value=100,
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


class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["./simulation/assets/js/HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = f"new HistogramModule({bins}, {canvas_width}, {canvas_height})"
        self.js_code = f"elements.push({new_element});"

    def render(self, model: KSUModel):
        gpa_vals = [student.gpa for student in model.schedule.agents]
        hist = tlz.first(np.histogram(gpa_vals, bins=self.bins))
        return [int(x) for x in hist]


canvas_grid = CanvasGrid(
    set_agent_params,
    GLOBAL_OPTS["width"],
    GLOBAL_OPTS["height"],
    GLOBAL_OPTS["width_pixels"],
    GLOBAL_OPTS["height_pixels"],
)

# avg_gpa_chart = ChartModule(
#     [{"Label": "Avg GPA", "Color": "Black"}], data_collector_name="datacollector"
# )

# hist_chart = HistogramModule(list(range(10)), 200, 500)

semester_code = SemesterElement()

server: ModularServer = ModularServer(
    KSUModel, [canvas_grid, semester_code], "KSU Simulation", model_params
)

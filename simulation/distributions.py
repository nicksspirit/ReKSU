import pandas as pd
import numpy as np
from typing import List
from pathlib import Path

DATA_PATH = Path.cwd().parent / "distributions" / "data"
majors_df = pd.read_csv(DATA_PATH / "major_prob.csv", index_col="F1SEQ1_MAJOR")

MAJOR_CODES = majors_df.index.values
MAJOR_PROBS = majors_df["Probability"].values


def gen_major(n_students: int) -> List[str]:
    majors = np.random.choice(
        MAJOR_CODES, size=n_students, replace=True, p=MAJOR_PROBS)

    return majors

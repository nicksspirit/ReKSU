import pandas as pd
import numpy as np
from typing import List
from pathlib import Path

DATA_PATH = Path.cwd().parent / "distributions" / "data"

majors_df = pd.read_csv(DATA_PATH / "f1seq1_major_probs.csv", index_col="F1SEQ1_MAJOR")
F1SEQ1_MAJOR_CODES = majors_df.index.values
F1SEQ1_MAJOR_PROBS = majors_df["Probability"].values


def gen_major(n_students: int, semester: str = "s1seq1") -> List[str]:

    if semester == "s1seq1":
        majors = np.random.choice(
            F1SEQ1_MAJOR_CODES, size=n_students, replace=True, p=F1SEQ1_MAJOR_PROBS
        )

    return majors


gender_df = pd.read_csv(DATA_PATH / "gender_probs.csv", index_col="GENDER")
GENDER = gender_df.index.values
GENDER_PROBS = gender_df["Probability"].values


def gen_gender(n_students: int) -> List[str]:
    majors = np.random.choice(GENDER, size=n_students, replace=True, p=GENDER_PROBS)

    return majors

import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
from pathlib import Path

DATA_PATH = Path.cwd() / "distributions" / "data"

# F1SEQ1_MAJORS (2011)

f1seq1_majors_df = pd.read_csv(
    DATA_PATH / "f1seq1_major_probs_2011.csv", index_col="F1SEQ1_MAJOR"
)
F1SEQ1_MAJOR_CODES = f1seq1_majors_df.index.values
F1SEQ1_MAJOR_PROBS = f1seq1_majors_df["P"].values


def gen_f1seq1_majors(n_students: int) -> List[str]:
    majors = np.random.choice(
        F1SEQ1_MAJOR_CODES, size=n_students, replace=True, p=F1SEQ1_MAJOR_PROBS
    )

    return majors


# Genders

gender_df = pd.read_csv(DATA_PATH / "gender_probs.csv", index_col="GENDER")
GENDER = gender_df.index.values
GENDER_PROBS = gender_df["Probability"].values


def gen_gender(n_students: int) -> List[str]:
    majors = np.random.choice(GENDER, size=n_students, replace=True, p=GENDER_PROBS)

    return majors


# Conditional Probabilities of MAJORS (2011)

# P(F1SEQ2_MAJOR | F1SEQ1_MAJOR)


class MajorSwitch:
    sem_major_df: Dict[Tuple[str, str], pd.DataFrame] = {}

    def __init__(self):
        self.sem_major_df[("F1SEQ1_MAJOR", "F1SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f1seq1_2_major_cprobs_2011.csv"
        )
        self.sem_major_df[("F1SEQ2_MAJOR", "S1SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f1_s1_seq2_major_cprobs_2011.csv"
        )
        self.sem_major_df[("S1SEQ2_MAJOR", "F2SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "s1_f2_seq2_major_cprobs_2011.csv"
        )
        self.sem_major_df[("F2SEQ2_MAJOR", "S2SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f2_s2_seq2_major_cprobs_2011.csv"
        )
        self.sem_major_df[("S2SEQ2_MAJOR", "F3SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "s2_f3_seq2_major_cprobs_2011.csv"
        )
        self.sem_major_df[("F3SEQ2_MAJOR", "S3SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f3_s3_seq2_major_cprobs_2011.csv"
        )
        self.sem_major_df[("S3SEQ2_MAJOR", "F4SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "s3_f4_seq2_major_cprobs_2011.csv"
        )
        self.sem_major_df[("F4SEQ2_MAJOR", "S4SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f4_s4_seq2_major_cprobs_2011.csv"
        )
        self.sem_major_df[("S4SEQ2_MAJOR", "F5SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "s4_f5_seq2_major_cprobs_2011.csv"
        )
        self.sem_major_df[("F5SEQ2_MAJOR", "S5SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f5_s5_seq2_major_cprobs_2011.csv"
        )
        self.sem_major_df[("S5SEQ2_MAJOR", "F6SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "s5_f6_seq2_major_cprobs_2011.csv"
        )
        self.sem_major_df[("F6SEQ2_MAJOR", "S6SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f6_s6_seq2_major_cprobs_2011.csv"
        )

    def get_major(self, prev_sem: str, next_sem: str, curr_major: str) -> str:
        """Get major for next semester given current major

        Args:
            prev_sem (str): current semester
            next_sem (str): semester for which you want the most probable major
            curr_major (str): major in the current semester

        Returns: most probable major
            str
        """
        if (prev_sem, next_sem) not in self.sem_major_df.keys():
            return curr_major

        sem_majors: pd.Dataframe = self.sem_major_df[(prev_sem, next_sem)].loc[
            lambda df: df[prev_sem] == curr_major
        ]

        if sem_majors.empty:
            return ""

        next_sem_major_probs = sem_majors["cProb"].values
        next_sem_majors = sem_majors[next_sem].values

        return np.random.choice(next_sem_majors, p=next_sem_major_probs)

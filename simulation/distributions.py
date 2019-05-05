import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Iterable, Generator
from pathlib import Path

DATA_PATH = Path.cwd() / "distributions" / "data"

# GPA (Weibull)

gpa_df = pd.read_csv(DATA_PATH / "gpa_weibull.csv", index_col="semester")


def gen_gpa(semester: str, n_students: int) -> List[str]:
    if semester not in gpa_df.index:
        return []

    scale, shape = gpa_df.loc[semester, :]

    return np.random.weibull(shape, n_students) * scale


# Earned & Attempted Credit Hours (Normal)


def gen_pos_normal(mean: float, std: float, size: int) -> Generator:
    count = size

    def rand_normal(mean: float, std: float) -> float:
        rand_n = np.random.normal(mean, std)

        if rand_n < 0:
            rand_n = rand_normal(mean, std)

        return rand_n

    while count != 0:
        yield rand_normal(mean, std)
        count -= 1


earned_hrs_df = pd.read_csv(DATA_PATH / "earned_hrs_normal.csv", index_col="semester")
attempted_hrs_df = pd.read_csv(
    DATA_PATH / "attempted_hrs_normal.csv", index_col="semester"
)


def gen_credit_hrs(semester: str, n_students: int, is_earned=True) -> Iterable[int]:
    credit_hr_df = earned_hrs_df if is_earned else attempted_hrs_df

    if semester not in credit_hr_df.index:
        return []

    mean, std = credit_hr_df.loc[semester, :]

    return gen_pos_normal(mean, std, n_students)


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
    sem_major: Dict[Tuple[str, str], pd.DataFrame] = {}

    def __init__(self):
        self.sem_major[("F1SEQ1_MAJOR", "F1SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f1seq1_2_major_cprobs_2011.csv"
        )
        self.sem_major[("F1SEQ2_MAJOR", "S1SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f1_s1_seq2_major_cprobs_2011.csv"
        )
        self.sem_major[("S1SEQ2_MAJOR", "F2SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "s1_f2_seq2_major_cprobs_2011.csv"
        )
        self.sem_major[("F2SEQ2_MAJOR", "S2SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f2_s2_seq2_major_cprobs_2011.csv"
        )
        self.sem_major[("S2SEQ2_MAJOR", "F3SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "s2_f3_seq2_major_cprobs_2011.csv"
        )
        self.sem_major[("F3SEQ2_MAJOR", "S3SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f3_s3_seq2_major_cprobs_2011.csv"
        )
        self.sem_major[("S3SEQ2_MAJOR", "F4SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "s3_f4_seq2_major_cprobs_2011.csv"
        )
        self.sem_major[("F4SEQ2_MAJOR", "S4SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f4_s4_seq2_major_cprobs_2011.csv"
        )
        self.sem_major[("S4SEQ2_MAJOR", "F5SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "s4_f5_seq2_major_cprobs_2011.csv"
        )
        self.sem_major[("F5SEQ2_MAJOR", "S5SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "f5_s5_seq2_major_cprobs_2011.csv"
        )
        self.sem_major[("S5SEQ2_MAJOR", "F6SEQ2_MAJOR")] = pd.read_csv(
            DATA_PATH / "s5_f6_seq2_major_cprobs_2011.csv"
        )
        self.sem_major[("F6SEQ2_MAJOR", "S6SEQ2_MAJOR")] = pd.read_csv(
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
        if (prev_sem, next_sem) not in self.sem_major.keys():
            return curr_major

        sem_majors: pd.Dataframe = self.sem_major[(prev_sem, next_sem)].loc[
            lambda df: df[prev_sem] == curr_major
        ]

        if sem_majors.empty:
            return ""

        next_sem_major_probs = sem_majors["cProb"].values
        next_sem_majors = sem_majors[next_sem].values

        return np.random.choice(next_sem_majors, p=next_sem_major_probs)

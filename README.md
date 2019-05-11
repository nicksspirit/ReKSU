# ReKSU
An agent based simulation on Kent State University's student retention


# Simulation Goal

Create a simulation to mirror the success of students over the course of 6 years going by semester to semester using distributions within the data. The goal is to gain insight on the trends that are preventing student success and identify those that are having trouble to provide support.

The Simulation mimicks the real system by considering the conditional probabilitiy of Majors and GPAs for consecutive semesters. It also looks at the distribution of GPAs based on full-time and part-time status of the student. The Simulation identifies the conditional probablitites for term attended hours, term earned hours and cumulative earned hours and their distributions across every semester and Major. Also the simulation introduces a major E, which is assigned to a student when the student exits the University.


# How to run it

1. First install all the depencies from the `Pipfile` using `pipenv`
2. Run the command `pipenv run sim` or run the `run.py` file using python3.6+

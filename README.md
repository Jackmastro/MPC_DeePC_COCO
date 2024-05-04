# COCO Project 2024

A codebase for testing different controllers using ReplayBG (Glucose concentration simulation).

All the necessary information is being presented on a Jupyter Notebook

# Installation

The codebase is made to be used in JupyterHub with Moodle. No installation is necessary.

# Usage

By using the Jupyter Notebook, it is possible to run the ReplayBG simulator with a basic controller, as well as a PID controller. More controller can be easily tested.

# Bug report

When you are runing the code, you may come across some RuntimeWarnings (`RuntimeWarning: Mean of empty slice`, `RuntimeWarning: invalid value encountered in scalar divide`). These warnings come from the `py_agata` module and are produced when there are no hyperglemic or hypoglemic events during the simulation, but the module still tries to produce metrics for these instances. The issue can be addressed by removing those metrics for the specific cases, but this would require the reinstallation of some packages on the hub, which takes time. Thus, as long as the warnings do not stop the code execution, we leave them as they are for now. In a future version, these warnings need to be addressed.

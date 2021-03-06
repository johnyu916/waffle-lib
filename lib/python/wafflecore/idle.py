import json
from plugins.jsonsyrup import SyrupEncoder
import math
import os.path
from random import random
from time import time
import numpy

from task import task_new_exec_wait
from bagel.task_run import task_run

def idle(state):
    now = time()
    delta = (now - state["now"])
    print_fps(state)
    state["now"] = now
    state["delta"] = delta
    if ((state["cycle"] % 100.0) == 0.0):
            print json.dumps(["cycle", state["cycle"]], cls=SyrupEncoder)
    state["cycle"] += 1.0
    state["tasks_next"] = []
    for task in state["tasks"]:
            if (task["status"] == "exit"):
                        for parent in task["signal_on_exit"]:
                                        parent["waiting_on"].remove(task)
                                        if (len(parent["waiting_on"]) == 0.0):
                                                            parent["status"] = "run"
                        continue
            if (task["status"] == "run"):
                        if (task["time_start"] == 0.0):
                                        task["time_start"] = now
                        task_run(state, task)
            state["tasks_next"].append(task)
    state["tasks"] = state["tasks_next"]
    return 

def print_fps(state):
    frame_time = (state["now"] - state["frame_start_time"])
    if (frame_time > 1.0):
            fps = (state["frames"] / frame_time)
            print json.dumps(["fps ", fps], cls=SyrupEncoder)
            state["frames"] = 0.0
            state["frame_start_time"] = state["now"]
    state["frames"] += 1.0
    return 


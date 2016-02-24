import json
from plugins.jsonsyrup import SyrupEncoder
import math
import os.path
from random import random
from time import time
import numpy

from wafflecore.compute import new_id

def get_task_old(state, name):
    value = {}
    for task in state["game"]["tasks"]:
            if (task["name"] == name):
                        value = task
                        return value
    value = None
    return value

def task_new(state, name):
    task = {}
    task = {"id" : new_id(state), "name" : name, "status" : "run", "signal_on_exit" : [], "waiting_on" : [], "time_start" : 0.0, "step" : 0.0, "animations" : {}}
    return task

def task_new_exec(state, name):
    task = {}
    task = task_new(state, name)
    state["tasks_next"].append(task)
    return task

def task_new_exec_wait(state, task, name):
    child_task = {}
    child_task = task_new_exec(state, name)
    task_wait(task, child_task)
    return child_task

def task_wait(task, child_task):
    child_task["signal_on_exit"].append(task)
    task["waiting_on"].append(child_task)
    task["status"] = "wait"
    return 

def task_exit(task, result):
    task["status"] = "exit"
    task["result"] = result
    return 


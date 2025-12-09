#!/usr/bin/env python3.10
import os
import time
import ray
from ray import remote
import math
import random

NUM_TASK = 10
NUM_SAMPLES_PER_TASK = 20_000_000
TOTAL_NUM_SAMPLES = NUM_TASK * NUM_SAMPLES_PER_TASK

# An actor in ray is stateful worker process that can store and update
# internal state across call
@remote
class ProgressActor:
    def __init__(self, total_num_samples):
        self.total_num_samples = total_num_samples
        self.num_samples_completed_per_task = {}
    
    def report_progress(self, task_id, num_sample_completed):
        self.num_samples_completed_per_task[task_id] = num_sample_completed
    

# stateless remote function call
@remote
def mc_step_task(num_samples, task_id, progress_actor):
    inside_circle_pts = 0
    for i in range(num_samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if math.hypot(x, y) <= 1:
            inside_circle_pts += 1
        
        # report progress every 1 million samples
        if (i + 1) % 1_000_000 == 0:
            # async operation
            progress_actor.report_progress.remote(task_id, i + 1)
    # report final progress
    progress_actor.report_progress.remote(task_id, num_samples)
    return inside_circle_pts


def simulate_mc_step(num_samples):
    inside_circle_pts = 0
    for i in range(num_samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if math.hypot(x, y) <= 1:
            inside_circle_pts += 1
        
        if (i + 1) % 1_000_000 == 0:
            # print(f"progress: {(i / TOTAL_NUM_SAMPLES)*100}")
            pass
    return inside_circle_pts


if not os.getenv("REMOTE"):
    print("serialized way")
    # without ray lib, it takes 50 secs
    start_time = time.time()
    addup  = 0
    for _ in range(NUM_TASK):
        addup += simulate_mc_step(NUM_SAMPLES_PER_TASK) 
    esitmated_pi = (4 * addup) / TOTAL_NUM_SAMPLES
    print(f"esitmated_pi: {esitmated_pi}") 
    print(f"end time: {time.time() - start_time}secs")
else:
    ray.init(address="ray://localhost:10001")
    print(f"nodes in cluster: {len(ray.nodes())}\n")
    # this only takes 16 secs. step for cluster - 1 head and 1 worker
    print("ray distributed way")
    start_time = time.time()
    progress_actor = ProgressActor.remote(TOTAL_NUM_SAMPLES)
    results = []
    for tid in range(NUM_TASK):
        val = mc_step_task.remote(NUM_SAMPLES_PER_TASK, tid, progress_actor)
        results.append(val)

    total_pts_inside = (sum(ray.get(results)))
    esitmated_pi = (4 * total_pts_inside) / TOTAL_NUM_SAMPLES
    print(f"esitmated_pi: {esitmated_pi}")
    print(f"end time: {time.time() - start_time}secs")


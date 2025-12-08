#!/usr/bin/env python3.10
from ray import remote
import ray
import time
import socket
# import cv2

# Make sure ray client python version is same as ray package version in cluster head machine
# if there is mismatch, the script won't run.
# Current docker image for ray uses python3.10.19

@remote
def some_func():
    time.sleep(0.001)
    return socket.gethostbyname(socket.gethostname())

@remote
def compute_cv2_image(img):
    orb = cv2.AKAZE_create()
    kp = orb.detect(img, None)
    kp, des = orb.compute(img, kp)
    return des


if __name__ == "__main__":
    ray.init(address="ray://localhost:10001")

    print(f"nodes in cluster: {len(ray.nodes())}\n")

    for rn in (ray.nodes()):
        print("NodeID:", rn["NodeID"])
        print("Alive:", rn["Alive"])
        print("NodeName:", rn["NodeName"])

    # init time counter
    start_time = time.time()
    process_ids =[]
    for _ in range(10000):
        process_ids.append(some_func.remote())
    ip_address = ray.get(process_ids)

    # this takes 31.44 seconds to finish program
    # but after we apply ray dsitributed process (running 2 nodes (1 master and 1 worker))
    # it only takes 7.99 seconds. < 31.44/2

    # for _ in range(10000):
    #     some_func()

    # img_path =  "pythonlogo.png"
    # process_ids = []
    # for _ in range(5000):
    #     # compute_cv2_image(cv2.imread(img_path)) 
    #     process_ids.append(compute_cv2_image.remote(cv2.imread(img_path)))
    # ip_address = ray.get(process_ids)

    # # print(des)
    
    print(f"endtime: {time.time() - start_time}")






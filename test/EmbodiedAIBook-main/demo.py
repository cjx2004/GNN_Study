import os
import cv2
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
import json

import ai2thor
from ai2thor.controller import Controller


def demo():
    sav_path = './tmp_data/'
    if not os.path.exists(sav_path):
        os.makedirs(sav_path, exist_ok = True)
    
    controller = Controller(
        scene = "FloorPlan221",
        gridSize = 0.25,
        rotateStepDegrees = 90,
        renderDepthImage = True,
        renderInstanceSegmentation = True,
        fieldOfView = 90
    )
    print("Start the controller.")

    num_step = 0
    event = controller.step(action = "GetReachablePositions")
    reachable_positions = event.metadata["actionReturn"]
    print(f"Reachable Points: {reachable_positions}")
    plt.imsave(os.path.join(sav_path, f'frame_{num_step}.png'), event.frame)
    num_step += 1

    event = controller.step(
        action = "Teleport",
        position = dict(x = -3.00, y = 0.9984914064407349, z = -2.25),
        rotation = dict(x = 0, y = 0, z = 0),
        horizon = 0,
        standing = True
    )
    print("Teleport {}".format(event.metadata["lastActionSuccess"]))
    plt.imsave(os.path.join(sav_path, f'frame_{num_step}.png'), event.frame)
    num_step += 1

    event = controller.step(
        action = "PickupObject",
        objectId = "Plate|-03.85|+00.88|-01.01"
    )
    print("PickUp Plate {}".format(event.metadata["lastActionSuccess"]))
    plt.imsave(os.path.join(sav_path, f'frame_{num_step}.png'), event.frame)
    num_step += 1

    nav_actions = ['MoveRight', 'MoveAhead', 'MoveRight', 'MoveRight', 'MoveAhead', 'MoveAhead', 
                   'MoveAhead', 'MoveAhead', 'MoveAhead', 'MoveAhead', 'MoveLeft', 'RotateRight']

    for act in nav_actions:
        event = controller.step(action = act)
        print("action:{} {}".format(act, event.metadata["lastActionSuccess"]))
        plt.imsave(os.path.join(sav_path, f'frame_{num_step}.png'), event.frame)
        num_step += 1

    event = controller.step(
        action = "PutObject",
        objectId = "CoffeeTable|-01.09|+00.10|-00.74"
    )
    print("Put Plate to CoffeeTable {}".format(event.metadata["lastActionSuccess"]))
    plt.imsave(os.path.join(sav_path, f'frame_{num_step}.png'), event.frame)
    num_step += 1

    event = controller.step(action = "GetMapViewCameraProperties", raise_for_failure = True)
    event = controller.step(
        action = "AddThirdPartyCamera",
        **event.metadata["actionReturn"]
    )
    top_down_frame = event.third_party_camera_frames[-1]
    print("Draw Top-Down View")
    plt.imsave(os.path.join(sav_path, f'top_down.png'), top_down_frame)
    

if __name__ == "__main__":
    demo()

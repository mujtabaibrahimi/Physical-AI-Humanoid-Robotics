# Chapter 6: Capstone Project

## Introduction

In this final chapter, you'll integrate everything learned throughout this textbook into a comprehensive capstone project: building an autonomous robot system that can perceive its environment, understand natural language commands, and execute physical tasks.

## Project Overview

**Goal**: Create a tabletop manipulation system that can:
1. Detect and recognize objects on a table
2. Understand natural language instructions
3. Plan and execute pick-and-place operations
4. Provide feedback on task progress

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    ROS 2 Humble                          │
├──────────────┬──────────────┬──────────────┬────────────┤
│  Perception  │   Language   │   Planning   │  Control   │
│    Node      │     Node     │    Node      │   Node     │
├──────────────┼──────────────┼──────────────┼────────────┤
│ RGB-D Camera │  VLA Model   │ MoveIt 2     │ Joint Ctrl │
│ YOLO v8      │  (OpenVLA)   │ RRT Planner  │ Gripper    │
└──────────────┴──────────────┴──────────────┴────────────┘
```

## Phase 1: Environment Setup

### Hardware Requirements (Simulation Alternative Available)

| Component | Options | Estimated Cost |
|-----------|---------|----------------|
| Robot Arm | UR3e, Franka, or AR4 (DIY) | $3,000-$30,000 |
| Gripper | Robotiq 2F-85 or 3D-printed | $500-$3,000 |
| Camera | Intel RealSense D435 | $300 |
| Compute | NVIDIA Jetson or Desktop GPU | $500-$2,000 |

### Simulation Setup (Isaac Sim)

```python
# capstone/simulation/setup_scene.py
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage

def create_tabletop_scene():
    """Initialize capstone project scene in Isaac Sim"""
    world = World(stage_units_in_meters=1.0)

    # Add table
    add_reference_to_stage(
        usd_path="omniverse://localhost/NVIDIA/Assets/Props/table.usd",
        prim_path="/World/Table"
    )

    # Add robot arm
    add_reference_to_stage(
        usd_path="omniverse://localhost/NVIDIA/Robots/UR/ur3e.usd",
        prim_path="/World/Robot"
    )

    # Add objects to manipulate
    objects = ["red_cube", "blue_cylinder", "green_sphere"]
    for i, obj in enumerate(objects):
        add_reference_to_stage(
            usd_path=f"omniverse://localhost/NVIDIA/Assets/Objects/{obj}.usd",
            prim_path=f"/World/Objects/{obj}"
        )

    return world
```

## Phase 2: Perception Pipeline

Build object detection and localization:

```python
# capstone/perception/detector.py
import cv2
import numpy as np
from ultralytics import YOLO

class ObjectDetector:
    """Detect and localize objects for manipulation"""

    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)
        self.class_names = ["cube", "cylinder", "sphere", "cup", "bottle"]

    def detect(self, rgb_image, depth_image, camera_intrinsics):
        """
        Detect objects and compute 3D positions

        Returns:
            List of detected objects with 3D positions
        """
        results = self.model(rgb_image)
        detections = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = box.conf[0].cpu().numpy()
                class_id = int(box.cls[0])

                # Get 3D position from depth
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                depth = depth_image[center_y, center_x]

                position_3d = self.deproject(
                    center_x, center_y, depth, camera_intrinsics
                )

                detections.append({
                    "class": self.class_names[class_id],
                    "confidence": float(confidence),
                    "bbox": [x1, y1, x2, y2],
                    "position": position_3d
                })

        return detections
```

## Coming Soon

This chapter is under development. Phases to be covered:

- **Phase 3**: Language understanding integration
- **Phase 4**: Motion planning with MoveIt 2
- **Phase 5**: Gripper control and grasping
- **Phase 6**: System integration and testing
- **Phase 7**: Evaluation and improvements

## Evaluation Criteria

Your capstone will be evaluated on:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Perception Accuracy | 20% | Object detection and localization |
| Language Understanding | 20% | Command interpretation accuracy |
| Task Success Rate | 30% | Successful pick-and-place operations |
| Code Quality | 15% | Clean, documented, tested code |
| Documentation | 15% | Clear README, design decisions |

---

## Resources

1. **Starter Code**:
   - GitHub repository (coming soon)
   - Pre-configured Isaac Sim scenes
   - ROS 2 package templates

2. **Support**:
   - Use the AI chatbot for concept clarification
   - Community forum for troubleshooting

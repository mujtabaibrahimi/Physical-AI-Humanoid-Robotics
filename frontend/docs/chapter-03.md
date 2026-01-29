# Chapter 3: ROS 2 Fundamentals

## Introduction

The Robot Operating System 2 (ROS 2) is the standard middleware for robotics development. Unlike its predecessor, ROS 2 is built on DDS (Data Distribution Service) for real-time, secure, and distributed communication.

## Why ROS 2?

| Feature | ROS 1 | ROS 2 |
|---------|-------|-------|
| Real-time support | No | Yes |
| Security | None | DDS Security |
| Multi-robot | Difficult | Native |
| Platform | Linux only | Linux, Windows, macOS |
| Lifecycle | None | Managed nodes |

## Core Concepts

### Nodes

Nodes are the fundamental units of computation in ROS 2. Each node should do one thing well.

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    """A simple ROS 2 publisher node"""

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()
```

### Topics

Topics are named buses for asynchronous, many-to-many communication.

### Services

Services provide synchronous request-response communication.

### Actions

Actions extend services with feedback during long-running tasks.

## Installation

### Ubuntu 22.04 (Recommended)

```bash
# Set locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8

# Setup sources
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y

# Add ROS 2 GPG key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | \
  sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 Humble
sudo apt update
sudo apt install ros-humble-desktop
```

## Coming Soon

This chapter is under development. Topics to be covered:

- Creating custom messages and services
- Launch files and parameters
- TF2 transforms
- Building packages with colcon
- Best practices for node design

---

## Further Reading

1. **Official Documentation**:
   - [ROS 2 Documentation](https://docs.ros.org/en/humble/)
   - [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)

2. **Books**:
   - *Programming Robots with ROS 2* (upcoming)

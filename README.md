# Max – Autonomous Mobile Robot (AMR)

**Max** is a 4-wheeled Autonomous Mobile Robot (AMR) designed for mapping and autonomous navigation using ROS 2 Humble Hawksbill.

## Features
* **Navigation:** Differential drive controller with full autonomous navigation using **Nav2**.
* **Mapping:**

  * **2D Mapping:** SLAM Toolbox with RPLIDAR A1.
  * **VSLAM:** RTAB-Map with Orbbec Astra Pro.

## Installation

```bash
# Create workspace
mkdir max_ws && cd max_ws

# Clone repository
git clone https://github.com/sierra-95/Max.git

# Move source files
mkdir src && mv Max src/

# Build workspace
colcon build

# Source setup
. install/setup.bash
```

## Running Max

### Simulated Robot

```bash
ros2 launch max_bringup max.simulated.launch.py
```

### Real Robot

```bash
ros2 launch max_bringup max.launch.py
```


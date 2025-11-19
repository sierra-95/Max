# Project Max

**Max** is a 4-wheeled Autonomous Mobile Robot (AMR) designed for mapping and autonomous navigation using ROS 2 Humble Hawksbill.

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

#### Simulated Robot

```bash
ros2 launch max_bringup max.simulated.launch.py
```

#### Real Robot

```bash
ros2 launch max_bringup max.launch.py
```


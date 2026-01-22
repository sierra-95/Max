# Project Max

**Max** is a 4-wheeled Autonomous Mobile Robot (AMR) designed for mapping and autonomous navigation using ROS 2 Humble Hawksbill.

## Getting Started

```bash
# Create workspace
mkdir max_ws && cd max_ws

# Clone repository
git clone https://github.com/sierra-95/Max.git

# Move source files
mkdir src && mv Max src/

```
## Installation

```bash
# Update Ros Database
sudo rosdep update

# Install dependancies
rosdep install --from-paths src --ignore-src -r -y
```

```bash
# Build the  packages
colcon build --symlink-install
. install/setup.bash
```
## Launching Max

#### Simulated Robot

```bash
ros2 launch max_bringup max.simulated.launch.py
```

#### Real Robot

```bash
ros2 launch max_bringup max.launch.py
```
ros2 launch rplidar_ros rplidar_a1_launch.py serial_port:=/dev/ttyUSB0 serial_baudrate:=115200 frame_id:=lidar_link

ros2 launch astra_camera astra_pro.launch.xml

ros2 launch rtabmap_demos robot_mapping_demo.launch.py \
  rviz:=true \
  rtabmap_viz:=true

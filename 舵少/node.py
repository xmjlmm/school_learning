/camera_node:
  ros__parameters:
    camera_info_url: package://rm_vision_bringup/config/camera_info.yaml
    exposure_time: 3500                     # 950
    gain: 15.0

/serial_driver:
  ros__parameters:
    timestamp_offset: 0.00
    device_name: /dev/ttyUSB0
    baud_rate: 115200
    flow_control: none
    parity: none
    stop_bits: "1"
    latency_time : 0.1

/armor_detector:
  ros__parameters:
    debug: true

    detect_color: 0
    binary_thres: 80

    light.min_ratio: 0.1
    armor.min_light_ratio: 0.8

    classifier_threshold: 0.8   # 0.8
    ignore_classes: ["","negative"]
#guard negative
/armor_tracker:
  ros__parameters:
    target_frame: odom
    max_armor_distance: 10.0

    ekf:
      sigma2_q_xyz: 0.05
      sigma2_q_yaw: 15.0
      sigma2_q_r: 80.0

      r_xyz_factor: 4e-4
      r_yaw: 5e-3

    tracker:
      max_match_distance: 0.5
      max_match_yaw_diff: 1.0

      tracking_thres: 5
      lost_time_thres: 1.0













/camera_node:
  ros__parameters:
    camera_info_url: package://rm_vision_bringup/config/camera_info.yaml
    exposure_time: 2000                       # 950
    gain: 15.0

/serial_driver:
  ros__parameters:
    timestamp_offset: -0.01       # -0.02
    device_name: /dev/ttyUSB0
    baud_rate: 115200
    flow_control: none
    parity: none
    stop_bits: "1"
    latency_time : 0.075  # 0.095

/armor_detector:
  ros__parameters:
    debug: true

    detect_color: 0
    binary_thres: 80

    light.min_ratio: 0.05
    armor.min_light_ratio: 0.8

    classifier_threshold: 0.8   # 0.8
    ignore_classes: ["","negative"]
#guard negative
/armor_tracker:
  ros__parameters:
    target_frame: odom
    max_armor_distance: 10.0

    ekf:
      sigma2_q_xyz: 0.005      # 0.05
      sigma2_q_yaw: 16.0     # 5.0
      sigma2_q_r: 80.0      # 80.0

      r_xyz_factor: 4e-4       # 1e-4
      r_yaw: 1e-2            # 5e-3

    tracker:
      max_match_distance: 0.5
      max_match_yaw_diff: 1.0

      tracking_thres: 2
      lost_time_thres: 0.5

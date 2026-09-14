"""Declarative settings panels mirroring sunnypilot BIG UI (15 panels)."""

from __future__ import annotations

from typing import Any

# Widget types: bool, int, choice, readonly, action, section, html, subpanel_ref

PANELS: list[dict[str, Any]] = [
  {
    "id": "device",
    "title": "Device",
    "custom": "device",
    "widgets": [
      {"type": "readonly", "param": "DongleId", "label": "Dongle ID"},
      {"type": "separator"},
      {"type": "readonly", "param": "HardwareSerial", "label": "Serial"},
      {"type": "separator"},
      {"type": "action", "action": "pair_device", "label": "Pair Device", "button": "PAIR",
       "desc": "Pair your device with comma connect (connect.comma.ai) and claim your comma prime offer.",
       "hide_when_paired": True},
      {"type": "separator"},
      {"type": "action", "action": "reset_calibration", "label": "Reset Calibration", "button": "RESET",
       "desc": "sunnypilot requires the device to be mounted within 4° left or right and within 5° up or 9° down.",
       "dynamic_desc": "calibration",
       "confirm": "Are you sure you want to reset calibration?"},
      {"type": "separator"},
      {"type": "custom", "custom": "device_language"},
      {"type": "separator"},
      {"type": "custom", "custom": "chestnut_status"},
      {"type": "multiple_button", "param": "DeviceBootMode", "label": "Wake Up Behavior",
       "buttons": ["Default", "Offroad"], "layout": "inline",
       "desc": "Controls state of the device after boot/sleep.\n\nDefault: Device will boot/wake-up normally & will be ready to engage.\nOffroad: Device will be in Always Offroad mode after boot/wake-up."},
      {"type": "separator"},
      {"type": "option", "param": "MaxTimeOffroad", "label": "Max Time Offroad",
       "desc": "Device will automatically shutdown after set time once the engine is turned off.\n(30h is the default)",
       "min": 0, "max": 11, "step": 1, "layout": "inline",
       "value_map": {"0": 0, "1": 5, "2": 10, "3": 15, "4": 30, "5": 60, "6": 120, "7": 180, "8": 300, "9": 600, "10": 1440, "11": 1800}},
      {"type": "dual_button",
       "left": {"label": "Quiet Mode", "param": "QuietMode", "toggle": True},
       "right": {"label": "Driver Camera Preview", "action": "driver_view", "offroad_only": True,
                 "desc": "Enable driver camera preview in Web UI while offroad. Turn off before driving."}},
      {"type": "dual_button",
       "left": {"label": "", "hidden": True},
       "right": {"label": "Onroad Preview", "action": "onroad_preview", "offroad_only": True}},
      {"type": "dual_button",
       "left": {"label": "Regulatory", "action": "open_regulatory", "offroad_only": True},
       "right": {"label": "Training Guide", "action": "open_training", "offroad_only": True}},
      {"type": "dual_button",
       "left": {"label": "Onroad Uploads", "param": "OnroadUploads", "toggle": True},
       "right": {"label": "Reset Settings", "action": "reset_all_params", "offroad_only": True, "confirm_twice": True}},
      {"type": "custom", "custom": "always_offroad"},
      {"type": "dual_button",
       "left": {"label": "Reboot", "action": "reboot"},
       "right": {"label": "Power Off", "action": "shutdown", "offroad_only": True, "hide_when_onroad": True}},
    ],
  },
  {
    "id": "imu_calibration",
    "title": "IMU Calibration",
    "custom": "imu_calibration",
    "widgets": [
      {"type": "bool", "param": "ImuCalibrationEnabled", "label": "Use IMU Calibration",
       "desc_i18n": "UseIMUCalibrationDescription",
       "needs_cycle": True},
      {"type": "action", "action": "imu_calibration_start", "label": "Start IMU Calibration", "button": "START",
       "desc_i18n": "StartIMUCalibrationDescription",
       "visible_if": {"param": "ImuCalibrationEnabled", "eq": "1"}},
      {"type": "action", "action": "imu_calibration_reset", "label": "Reset IMU Calibration", "button": "RESET",
       "desc_i18n": "ResetIMUCalibrationDescription",
       "confirm": "Are you sure you want to clear the IMU calibration and switch back to stock calibration?",
       "visible_if": {"param": "ImuCalibrationEnabled", "eq": "1"}},
    ],
  },
  {
    "id": "network",
    "title": "Network",
    "custom": "network",
    "widgets": [
      {"type": "subpanel", "target": "network__advanced", "label": "Advanced Network", "button": "ADVANCED"},
    ],
  },
  {
    "id": "sunnylink",
    "title": "sunnylink",
    "custom": "sunnylink",
    "widgets": [],
  },
  {
    "id": "toggles",
    "title": "Toggles",
    "widgets": [
      {"type": "bool", "param": "OpenpilotEnabledToggle", "label": "Enable sunnypilot", "needs_cycle": True,
       "icon": "selfdrive/assets/icons/chffr_wheel.png",
       "desc": "Use the sunnypilot system for adaptive cruise control and lane keep driver assistance. Your attention is required at all times to use this feature."},
      {"type": "bool", "param": "ExperimentalMode", "label": "Experimental Mode", "confirm_experimental": True,
       "capability": "longitudinal",
       "icon": "selfdrive/assets/icons/experimental_white.png",
       "icon_active": "selfdrive/assets/icons/experimental.png"},
      {"type": "bool", "param": "DisengageOnAccelerator", "label": "Disengage on Accelerator Pedal",
       "icon": "selfdrive/assets/icons/disengage_on_accelerator.png",
       "desc": "When enabled, pressing the accelerator pedal will disengage sunnypilot."},
      {"type": "multiple_button", "param": "LongitudinalPersonality", "label": "Driving Personality",
       "layout": "stacked", "capability": "longitudinal",
       "icon": "selfdrive/assets/icons/speed_limit.png",
       "buttons": ["Aggressive", "Standard", "Relaxed"],
       "desc": "Standard is recommended. In aggressive mode, sunnypilot will follow lead cars closer and be more aggressive with the gas and brake. In relaxed mode sunnypilot will stay further away from lead cars. On supported cars, you can cycle through these personalities with your steering wheel distance button."},
      {"type": "bool", "param": "IsLdwEnabled", "label": "Enable Lane Departure Warnings",
       "icon": "selfdrive/assets/icons/warning.png",
       "desc": "Receive alerts to steer back into the lane when your vehicle drifts over a detected lane line without a turn signal activated while driving over 31 mph (50 km/h)."},
      {"type": "bool", "param": "DisableDM", "label": "Disable Driver Monitoring", "needs_cycle": True,
       "icon": "selfdrive/assets/icons/monitoring.png",
       "desc": "Disable driver monitoring (no cabin camera required). Similar to LITE mode."},
      {"type": "bool", "param": "AlwaysOnDM", "label": "Always-On Driver Monitoring",
       "icon": "selfdrive/assets/icons/monitoring.png",
       "hide_if": {"param": "DisableDM", "eq": "1"},
       "desc": "The driver monitoring system can be toggled on/off, but long-term activation is recommended"},
      {"type": "multiple_button", "param": "DistractionDetectionLevel", "label": "Distraction Detection Level",
       "layout": "stacked",
       "icon": "selfdrive/assets/icons/monitoring.png",
       "buttons": ["Strict", "Moderate", "Lenient"],
       "visible_if": {"param": "AlwaysOnDM", "eq": "1"},
       "hide_if": {"param": "DisableDM", "eq": "1"},
       "desc": "Set how sensitive the driver distraction detection should be. Strict: Very sensitive, warns on minor distractions. Moderate: Balanced between sensitivity and false positives. Lenient: Only alerts on clear distractions."},
      {"type": "bool", "param": "RecordFront", "label": "Record and Upload Driver Camera", "needs_cycle": True,
       "icon": "selfdrive/assets/icons/monitoring.png",
       "hide_if": {"param": "DisableDM", "eq": "1"},
       "desc": "Upload data from the driver facing camera and help improve the driver monitoring algorithm."},
      {"type": "bool", "param": "RecordAudio", "label": "Record and Upload Microphone Audio", "needs_cycle": True,
       "icon": "selfdrive/assets/icons/microphone.png",
       "desc": "Record and store microphone audio while driving. The audio will be included in the dashcam video in comma connect."},
      {"type": "bool", "param": "SpDevBeep", "label": "Beeper Feedback", "lite_only": True, "needs_cycle": True,
       "icon": "selfdrive/assets/icons/warning.png",
       "desc": "Use the GPIO beeper for engage/disengage sounds on Lite hardware without a speaker."},
      {"type": "bool", "param": "IsMetric", "label": "Use Metric System",
       "icon": "selfdrive/assets/icons/metric.png",
       "desc": "Display speed in km/h instead of mph."},
    ],
  },
  {
    "id": "software",
    "title": "Software",
    "custom": "software",
    "widgets": [
      {"type": "action", "action": "uninstall", "label": "Uninstall", "button": "UNINSTALL",
       "confirm": "Are you sure you want to uninstall?", "offroad_only": True},
      {"type": "custom", "custom": "webui_update"},
      {"type": "bool", "param": "DisableUpdates", "label": "Disable Updates",
       "visible_if": {"param": "ShowAdvancedControls", "eq": "1"}, "offroad_only": True},
    ],
  },
  {
    "id": "models",
    "title": "Models",
    "custom": "models",
    "widgets": [
      {"type": "action", "action": "models_sync", "label": "Refresh Model List", "button": "REFRESH"},
      {"type": "action", "action": "models_clear_cache", "label": "Clear Model Cache", "button": "CLEAR",
       "confirm": "This will delete ALL downloaded models from the cache except the currently active model. Are you sure?",
       "confirm_button": "Clear Cache"},
      {"type": "bool", "param": "LaneTurnDesire", "label": "Use Lane Turn Desires",
       "desc": "If you're driving at 20 mph (32 km/h) or below and have your blinker on, the car will plan a turn in that direction at the nearest drivable path. This prevents situations (like at red lights) where the car might plan the wrong turn direction."},
      {"type": "option", "param": "LaneTurnValue", "label": "Adjust Lane Turn Speed",
       "min": 500, "max": 2000, "step": 100, "label_format": "lane_turn_speed",
       "desc": "Set the maximum speed for lane turn desires. Default is 19 mph.",
       "visible_if": {"param": "LaneTurnDesire", "eq": "1"},
       "advanced_if": {"param": "ShowAdvancedControls", "eq": "1"}},
      {"type": "bool", "param": "LagdToggle", "label": "Live Learning Steer Delay",
       "desc": "Enable this for the car to learn and adapt its steering response time. Disable to use a fixed steering response time. Keeping this on provides the stock openpilot experience."},
      {"type": "option", "param": "LagdToggleDelay", "label": "Adjust Software Delay",
       "min": 5, "max": 50, "step": 1, "label_format": "lagd_delay",
       "desc": "Adjust the software delay when Live Learning Steer Delay is toggled off. The default software delay value is 0.2",
       "visible_if": {"param": "LagdToggle", "eq": "0"},
       "advanced_if": {"param": "ShowAdvancedControls", "eq": "1"}},
      {"type": "option", "param": "CameraOffset", "label": "Adjust Camera Offset",
       "min": -35, "max": 35, "step": 1, "label_format": "camera_offset",
       "desc": "Virtually shift camera's perspective to move model's center to Left(+ values) or Right (- values)",
       "visible_if": {"state": "custom_model_active"}},
    ],
  },
  {
    "id": "steering",
    "title": "Steering",
    "widgets": [
      {"type": "bool", "param": "Mads", "label": "Modular Assistive Driving System (MADS)", "offroad_only": True,
       "desc": "Enable the beloved MADS feature. Disable toggle to revert back to stock sunnypilot engagement/disengagement."},
      {"type": "subpanel", "target": "steering__mads", "label": "Customize MADS", "button": "CUSTOMIZE",
       "requires": {"param": "Mads", "eq": "1"}, "offroad_only": True},
      {"type": "separator"},
      {"type": "subpanel", "target": "steering__lane_change", "label": "Customize Lane Change", "button": "CUSTOMIZE"},
      {"type": "separator"},
      {"type": "bool", "param": "BlinkerPauseLateralControl", "label": "Pause Lateral Control with Blinker",
       "desc": "Pause lateral control with blinker when traveling below the desired speed selected."},
      {"type": "option", "param": "BlinkerMinLateralControlSpeed", "label": "Minimum Speed to Pause Lateral Control",
       "min": 0, "max": 255, "step": 5, "label_format": "blinker_min_speed", "layout": "stacked",
       "visible_if": {"param": "BlinkerPauseLateralControl", "eq": "1"}},
      {"type": "option", "param": "BlinkerLateralReengageDelay", "label": "Post-Blinker Delay",
       "min": 0, "max": 10, "step": 1, "label_format": "blinker_delay", "layout": "stacked",
       "desc": "Delay before lateral control resumes after the turn signal ends.",
       "visible_if": {"param": "BlinkerPauseLateralControl", "eq": "1"}},
      {"type": "separator"},
      {"type": "bool", "param": "EnforceTorqueControl", "label": "Enforce Torque Lateral Control",
       "offroad_only": True, "capability": "torque_allowed",
       "desc": "Enable this to enforce sunnypilot to steer with Torque lateral control."},
      {"type": "subpanel", "target": "steering__torque", "label": "Customize Torque Params", "button": "CUSTOMIZE",
       "requires": {"param": "EnforceTorqueControl", "eq": "1"}},
      {"type": "separator"},
      {"type": "bool", "param": "NeuralNetworkLateralControl", "label": "Neural Network Lateral Control (NNLC)",
       "offroad_only": True, "capability": "torque_allowed"},
    ],
  },
  {
    "id": "cruise",
    "title": "Cruise",
    "widgets": [
      {"type": "bool", "param": "IntelligentCruiseButtonManagement", "label": "Intelligent Cruise Button Management (ICBM) (Alpha)",
       "offroad_only": True, "dynamic_desc": "icbm",
       "desc": "When enabled, sunnypilot will attempt to manage the built-in cruise control buttons by emulating button presses for limited longitudinal control."},
      {"type": "bool", "param": "DynamicExperimentalControl", "label": "Enable Dynamic Experimental Control",
       "desc": "Let the model decide when to use sunnypilot ACC or sunnypilot End to End Longitudinal.",
       "capability": "longitudinal"},
      {"type": "bool", "param": "SmartCruiseControlVision", "label": "Smart Cruise Control - Vision",
       "desc": "Use vision path predictions to estimate the appropriate speed to drive through turns ahead.",
       "capability": "scc"},
      {"type": "bool", "param": "SmartCruiseControlMap", "label": "Smart Cruise Control - Map",
       "desc": "Use map data to estimate the appropriate speed to drive through turns ahead.",
       "capability": "scc"},
      {"type": "bool", "param": "CustomAccIncrementsEnabled", "label": "Custom ACC Speed Increments",
       "offroad_only": True, "dynamic_desc": "custom_acc",
       "desc": "Enable custom Short & Long press increments for cruise speed increase/decrease.",
       "capability": "custom_acc"},
      {"type": "int", "param": "CustomAccShortPressIncrement", "label": "Short Press Increment", "min": 1, "max": 10, "step": 1,
       "visible_if": {"param": "CustomAccIncrementsEnabled", "eq": "1"}, "capability": "custom_acc"},
      {"type": "option", "param": "CustomAccLongPressIncrement", "label": "Long Press Increment",
       "min": 1, "max": 3, "step": 1, "label_format": "acc_long_press",
       "value_map": {"1": 1, "2": 5, "3": 10},
       "visible_if": {"param": "CustomAccIncrementsEnabled", "eq": "1"}, "capability": "custom_acc"},
      {"type": "subpanel", "target": "cruise__sla", "label": "Speed Limit", "button": "CUSTOMIZE"},
      {"type": "subpanel", "target": "cruise__longitudinal_mpc_tuning", "label": "Longitudinal MPC Tuning", "button": "CUSTOMIZE",
       "capability": "longitudinal"},
    ],
  },
  {
    "id": "navigation",
    "title": "Navigation",
    "widgets": [
      {"type": "bool", "param": "AmapEnabled", "label": "Enable Amap Navigation", "offroad_only": True,
       "desc": "Use Amap (Gaode) navigation data for map-based features."},
      {"type": "bool", "param": "CarrotEnabled", "label": "Enable Carrot Navigation", "offroad_only": True,
       "desc": "Use Carrot navigation data for map-based features."},
      {"type": "bool", "param": "CarrotNaviV2Enabled", "label": "Enable Carrot Navi v2 (7714)", "offroad_only": True,
       "visible_if": {"param": "CarrotEnabled", "eq": "1"},
       "desc": "Use the 7714 WebSocket v2 rich navigation stream (traffic, lanes, crossroad images)."},
      {"type": "int", "param": "CarrotManUdpPort", "label": "Carrot UDP Port", "min": 1024, "max": 65535, "step": 1,
       "offroad_only": True,
       "desc": "UDP port the Carrot companion app pushes navigation data to. Must match the port configured in the app (0 disables)."},
      {"type": "bool", "param": "CarrotWebEnabled", "label": "Carrot Web Panel", "offroad_only": True,
       "desc": "Serve the carrot tuning page (/nav_params) and four-corner radar visualisation (/radar) on port 8088."},
      {"type": "readonly", "param": "CarName", "label": "Car Model",
       "desc": "Identified car model, sent automatically with Carrot FTP uploads and shown in the companion app."},
      {"type": "custom", "custom": "amap_api_key", "label": "Amap API Key", "offroad_only": True,
       "desc": "API key for Amap services. Tap EDIT to enter or update the key."},
      {"type": "separator"},
      {"type": "multiple_button", "param": "CarrotPanelSide", "label": "Carrot Nav Panel Side",
       "offroad_only": True,
       "buttons": ["Left", "Right"],
       "desc": "Place the onroad Carrot navigation panel on the left or right side of the screen."},
      {"type": "int", "param": "CarrotPanelOpacity", "label": "Carrot Nav Panel Opacity",
       "min": 10, "max": 100, "step": 5, "offroad_only": True,
       "desc": "Opacity of the onroad Carrot navigation panel, in percent. Default 100."},
      {"type": "custom", "custom": "navigation_provider", "label": "Map Provider",
       "desc": "Current map data source used for speed limits and road names. Amap requires an API key to be set above."},
      {"type": "custom", "custom": "carrot_navi_debug", "label": "Carrot Navi Debug",
       "desc": "View the last navigation event summary handled by CarrotManager."},
      {"type": "separator"},
      {"type": "multiple_button", "param": "MyDrivingMode", "label": "Carrot Driving Mode",
       "visible_if": {"param": "CarrotEnabled", "eq": "1"},
       "buttons": ["Eco", "Normal", "Sport", "Safe"],
       "desc": "Carrot driving style preset."},
      {"type": "multiple_button", "param": "TrafficLightDetectMode", "label": "Traffic Light Assist",
       "visible_if": {"param": "CarrotEnabled", "eq": "1"},
       "buttons": ["Off", "Red Stop", "Red Stop + Green Go"],
       "desc": "Stop at red lights and optionally resume on green when using model-based stop line detection."},
      {"type": "bool", "param": "CarrotCurveSpeedEnabled", "label": "Navigation Curve Speed", "default": True,
       "visible_if": {"param": "CarrotEnabled", "eq": "1"},
       "desc": "Slow down for curves using navigation route curvature."},
      {"type": "bool", "param": "CarrotNavCruiseSpeedEnabled", "label": "Navigation Cruise Speed", "default": True,
       "visible_if": {"param": "CarrotEnabled", "eq": "1"},
       "desc": "Use navigation desired speed to limit cruise set speed."},
      {"type": "bool", "param": "CarrotHudInfoEnabled", "label": "Extended HUD Info", "default": True,
       "visible_if": {"param": "CarrotEnabled", "eq": "1"},
       "desc": "Show blind spot state, side vehicle distance, and traffic light info on the HUD."},
      {"type": "subpanel", "target": "navigation__carrot_tuning", "label": "Carrot Tuning", "button": "CUSTOMIZE"},
    ],
  },
  {
    "id": "visuals",
    "title": "Visuals",
    "widgets": [
      {"type": "bool", "param": "BlindSpot", "label": "Show Blind Spot Warnings",
       "desc": "Enabling this will display warnings when a vehicle is detected in your blind spot as long as your car has BSM supported."},
      {"type": "bool", "param": "TorqueBar", "label": "Steering Arc",
       "desc": "Display steering arc on the driving screen when lateral control is enabled."},
      {"type": "bool", "param": "RainbowMode", "label": "Enable Tesla Rainbow Mode",
       "desc": "A beautiful rainbow effect on the path the model wants to take. It does not affect driving in any way."},
      {"type": "bool", "param": "StandstillTimer", "label": "Enable Standstill Timer",
       "desc": "Show a timer on the HUD when the car is at a standstill."},
      {"type": "bool", "param": "RoadNameToggle", "label": "Display Road Name",
       "desc": "Displays the name of the road the car is traveling on. The OpenStreetMap database of the location must be downloaded from the OSM panel to fetch the road name."},
      {"type": "bool", "param": "GreenLightAlert", "label": "Green Traffic Light Alert (Beta)",
       "desc": "A chime and on-screen alert will play when the traffic light you are waiting for turns green and you have no vehicle in front of you. Note: This chime is only designed as a notification. It is the driver's responsibility to observe their environment and make decisions accordingly."},
      {"type": "bool", "param": "LeadDepartAlert", "label": "Lead Departure Alert (Beta)",
       "desc": "A chime and on-screen alert will play when you are stopped, and the vehicle in front of you start moving. Note: This chime is only designed as a notification. It is the driver's responsibility to observe their environment and make decisions accordingly."},
      {"type": "bool", "param": "TrueVEgoUI", "label": "Speedometer: Always Display True Speed",
       "desc": "For applicable vehicles, always display the true vehicle current speed from wheel speed sensors."},
      {"type": "bool", "param": "HideVEgoUI", "label": "Speedometer: Hide from Onroad Screen",
       "desc": "When enabled, the speedometer on the onroad screen is not displayed."},
      {"type": "bool", "param": "ShowTurnSignals", "label": "Display Turn Signals",
       "desc": "When enabled, visual turn indicators are drawn on the HUD."},
      {"type": "bool", "param": "RocketFuel", "label": "Real-time Acceleration Bar",
       "desc": "Show an indicator on the left side of the screen to display real-time vehicle acceleration and deceleration. This displays what the car is currently doing, not what the planner is requesting."},
      {"type": "multiple_button", "param": "ChevronInfo", "label": "Display Metrics Below Chevron",
       "dynamic_desc": "chevron", "capability": "longitudinal",
       "buttons": ["Off", "Distance", "Speed", "Time", "All"]},
      {"type": "multiple_button", "param": "DevUIInfo", "label": "Developer UI",
       "desc": "Display real-time parameters and metrics from various sources.",
       "buttons": ["Off", "Bottom", "Right", "Right & Bottom"]},
    ],
  },
  {
    "id": "display",
    "title": "Display",
    "widgets": [
      {"type": "option", "param": "Brightness", "label": "Screen Brightness",
       "min": 0, "max": 100, "step": 5, "label_format": "offroad_brightness", "layout": "inline",
       "desc": "Screen brightness when offroad (not driving). 0 uses the device default (50%)."},
      {"type": "option", "param": "OnroadScreenOffBrightness", "label": "Onroad Brightness",
       "min": 0, "max": 22, "step": 1, "label_format": "onroad_brightness", "layout": "inline"},
      {"type": "option", "param": "OnroadScreenOffTimer", "label": "Onroad Brightness Delay",
       "min": 0, "max": 9, "step": 1, "label_format": "onroad_brightness_timer",
       "value_map": {"0": 0, "1": 3, "2": 5, "3": 10, "4": 15, "5": 30,
                     "6": 60, "7": 180, "8": 300, "9": 600},
       "layout": "inline"},
      {"type": "option", "param": "InteractivityTimeout", "label": "Interactivity Timeout",
       "min": 0, "max": 120, "step": 10, "label_format": "interactivity_timeout",
       "desc": "Apply a custom timeout for settings UI. This is the time after which settings UI closes automatically if user is not interacting with the screen.",
       "layout": "inline"},
      {"type": "bool", "param": "HideFirehosePrompt", "label": "Hide Firehose Prompt",
       "desc": "Hide the Firehose prompt on the home screen. The prompt will not be rendered when this is enabled."},
      {"type": "bool", "param": "ScreenSaverEnabled", "label": "Screen Saver",
       "desc": "Show a screen saver when the device is offroad and idle, instead of turning the screen off."},
      {"type": "option", "param": "ScreenSaverTimeout", "label": "Screen Saver Duration",
       "min": 60, "max": 600, "step": 60, "label_format": "screensaver_timeout",
       "desc": "How long the screen saver runs before the screen turns off.",
       "visible_if": {"param": "ScreenSaverEnabled", "eq": "1"}},
      {"type": "separator"},
      {"type": "custom", "custom": "stream_headless_mode", "desc_i18n": "webui_headless_mode_desc"},
      {"type": "custom", "custom": "stream_preview_quality", "desc_i18n": "webui_preview_quality_desc"},
      {"type": "custom", "custom": "stream_webcodecs"},
      {"type": "custom", "custom": "stream_diagnostics"},
    ],
  },
  {
    "id": "storage",
    "title": "Storage",
    "custom": "storage",
    "widgets": [],
  },
  {
    "id": "osm",
    "title": "OSM",
    "custom": "osm",
    "widgets": [],
  },
  {
    "id": "trips",
    "title": "Trips",
    "custom": "trips",
    "widgets": [],
  },
  {
    "id": "vehicle",
    "title": "Vehicle",
    "custom": "vehicle",
    "widgets": [],
  },
  {
    "id": "firehose",
    "title": "Data",
    "custom": "firehose",
    "widgets": [],
  },
  {
    "id": "developer",
    "title": "Developer",
    "widgets": [
      {"type": "bool", "param": "AdbEnabled", "label": "Enable ADB", "offroad_only": True,
       "desc": "ADB (Android Debug Bridge) allows connecting to your device over USB or over the network. See https://docs.comma.ai/how-to/connect-to-comma for more info."},
      {"type": "bool", "param": "SshEnabled", "label": "Enable SSH"},
      {"type": "custom", "custom": "ssh_keys", "label": "SSH Keys"},
      {"type": "bool", "param": "JoystickDebugMode", "label": "Joystick Debug Mode",
       "offroad_only": True, "capability": "not_release"},
      {"type": "bool", "param": "LongitudinalManeuverMode", "label": "Longitudinal Maneuver Mode",
       "offroad_only": True, "capability": "longitudinal_not_release"},
      {"type": "bool", "param": "LateralManeuverMode", "label": "Lateral Maneuver Mode",
       "offroad_only": True, "capability": "not_release"},
      {"type": "bool", "param": "AlphaLongitudinalEnabled", "label": "sunnypilot Longitudinal Control (Alpha)",
       "needs_cycle": True, "offroad_only": True, "capability": "alpha_longitudinal",
       "desc": "WARNING: sunnypilot longitudinal control is in alpha for this car and may disable Automatic Emergency Braking (AEB). On this car, sunnypilot defaults to the car's built-in ACC instead of sunnypilot's longitudinal control. Enable this to switch to sunnypilot longitudinal control. Enabling Experimental mode is recommended when enabling sunnypilot longitudinal control alpha. Changing this setting will restart sunnypilot if the car is powered on."},
      {"type": "bool", "param": "ShowDebugInfo", "label": "UI Debug Mode", "capability": "not_release"},
      {"type": "bool", "param": "ShowAdvancedControls", "label": "Show Advanced Controls",
       "desc": "Toggle visibility of advanced sunnypilot controls. This only changes the visibility of the toggles; it does not change the actual enabled/disabled state."},
      {"type": "bool", "param": "EnableGithubRunner", "label": "GitHub Runner Service",
       "desc": "Enables or disables the GitHub runner service.",
       "visible_if": {"param": "ShowAdvancedControls", "eq": "1"}, "capability": "not_release"},
      {"type": "bool", "param": "EnableCopyparty", "label": "copyparty Service",
       "desc": "copyparty is a very capable file server, you can use it to download your routes, view your logs and even make some edits on some files from your browser. Requires you to connect to your comma locally via its IP address.",
       "visible_if": {"param": "ShowAdvancedControls", "eq": "1"}},
      {"type": "bool", "param": "QuickBootToggle", "label": "Quickboot Mode",
       "visible_if": {"param": "ShowAdvancedControls", "eq": "1"}, "capability": "not_release_or_tested"},
      {"type": "action", "action": "developer_error_log", "label": "Error Log", "button": "VIEW",
       "capability": "not_release"},
    ],
  },
]

SUBPANELS: dict[str, dict[str, Any]] = {
  "navigation__carrot_tuning": {
    "id": "navigation__carrot_tuning",
    "title": "Carrot 调参",
    "parent": "navigation",
    "widgets": [
      {"type": "tabs", "tabs": ["开始", "巡航", "导航", "速度", "调节", "显示", "轨迹", "车辆", "开发者"], "default": "开始"},
      {"type": "tab", "tab": "开始", "widgets": [
        {
          "type": "section",
          "label": "自动起步 / 巡航"
        },
        {
          "type": "int",
          "param": "AutoEngage",
          "label": "自动开启辅助驾驶",
          "desc": "自动开启辅助驾驶 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoCruiseControl",
          "label": "自动设定巡航速度",
          "desc": "自动设定巡航速度 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "int",
          "param": "CruiseOnDist",
          "label": "达到设定距离自动开启",
          "desc": "达到设定距离自动开启 参数。",
          "min": 0,
          "max": 300,
          "step": 5
        },
        {
          "type": "int",
          "param": "CruiseEcoControl",
          "label": "经济巡航控制",
          "desc": "经济巡航控制 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "按钮行为"
        },
        {
          "type": "int",
          "param": "CruiseButtonMode",
          "label": "巡航按钮模式",
          "desc": "巡航按钮模式 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "int",
          "param": "CancelButtonMode",
          "label": "取消按钮模式",
          "desc": "取消按钮模式 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "int",
          "param": "SoftHoldOnCancel",
          "label": "取消后自动驻车",
          "desc": "取消后自动驻车 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "int",
          "param": "CruiseButtonLongDelay",
          "label": "巡航按钮长按延迟",
          "desc": "巡航按钮长按延迟 参数。",
          "min": 0,
          "max": 200,
          "step": 5
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "速度预设"
        },
        {
          "type": "int",
          "param": "CruiseSpeed1",
          "label": "巡航预设速度 1",
          "desc": "巡航预设速度 1 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "CruiseSpeed2",
          "label": "巡航预设速度 2",
          "desc": "巡航预设速度 2 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "CruiseSpeed3",
          "label": "巡航预设速度 3",
          "desc": "巡航预设速度 3 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "CruiseSpeed4",
          "label": "巡航预设速度 4",
          "desc": "巡航预设速度 4 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "CruiseSpeed5",
          "label": "巡航预设速度 5",
          "desc": "巡航预设速度 5 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "CruiseSpeedUnit",
          "label": "巡航预设速度单位",
          "desc": "巡航预设速度单位 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "CruiseSpeedUnitBasic",
          "label": "基础巡航预设速度单位",
          "desc": "基础巡航预设速度单位 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "方向盘按钮"
        },
        {
          "type": "int",
          "param": "LfaButtonMode",
          "label": "车道保持按钮模式",
          "desc": "车道保持按钮模式 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "int",
          "param": "PaddleMode",
          "label": "换挡拨片模式",
          "desc": "换挡拨片模式 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "自动油门"
        },
        {
          "type": "int",
          "param": "AutoGasCancelSpeed",
          "label": "自动油门取消速度",
          "desc": "自动油门取消速度 参数。",
          "min": 0,
          "max": 200,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoGasSyncSpeed",
          "label": "自动油门同步速度",
          "desc": "自动油门同步速度 参数。",
          "min": 0,
          "max": 200,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoGasTokSpeed",
          "label": "自动油门接管速度",
          "desc": "自动油门接管速度 参数。",
          "min": 0,
          "max": 200,
          "step": 5
        },
      ]},
      {"type": "tab", "tab": "巡航", "widgets": [
        {
          "type": "section",
          "label": "跟车距离"
        },
        {
          "type": "text",
          "param": "TFollowGap1",
          "label": "跟车时距 1",
          "desc": "跟车时距 1 参数。"
        },
        {
          "type": "text",
          "param": "TFollowGap2",
          "label": "跟车时距 2",
          "desc": "跟车时距 2 参数。"
        },
        {
          "type": "text",
          "param": "TFollowGap3",
          "label": "跟车时距 3",
          "desc": "跟车时距 3 参数。"
        },
        {
          "type": "text",
          "param": "TFollowGap4",
          "label": "跟车时距 4",
          "desc": "跟车时距 4 参数。"
        },
        {
          "type": "text",
          "param": "DynamicTFollow",
          "label": "动态跟车时距",
          "desc": "动态跟车时距 参数。"
        },
        {
          "type": "text",
          "param": "DynamicTFollowLC",
          "label": "变道时动态跟车时距",
          "desc": "变道时动态跟车时距 参数。"
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "纵向增益"
        },
        {
          "type": "int",
          "param": "LeadAccelResponse",
          "label": "前车加速响应",
          "desc": "前车加速响应 参数。",
          "min": -100,
          "max": 100,
          "step": 5
        },
        {
          "type": "int",
          "param": "LongActuatorDelay",
          "label": "纵向执行器延迟补偿",
          "desc": "纵向执行器延迟补偿 参数。",
          "min": 0,
          "max": 200,
          "step": 5
        },
        {
          "type": "int",
          "param": "LongTuningKf",
          "label": "纵向前馈系数",
          "desc": "纵向前馈系数 参数。",
          "min": 0,
          "max": 300,
          "step": 5
        },
        {
          "type": "int",
          "param": "LongTuningKiV",
          "label": "纵向积分速度系数",
          "desc": "纵向积分速度系数 参数。",
          "min": 0,
          "max": 300,
          "step": 5
        },
        {
          "type": "int",
          "param": "LongTuningKpV",
          "label": "纵向比例速度系数",
          "desc": "纵向比例速度系数 参数。",
          "min": 0,
          "max": 300,
          "step": 5
        },
        {
          "type": "int",
          "param": "StoppingAccel",
          "label": "停车加速度",
          "desc": "停车加速度 参数。",
          "min": -200,
          "max": 0,
          "step": 5
        },
        {
          "type": "int",
          "param": "TFollowDecelBoost",
          "label": "跟车减速增强",
          "desc": "跟车减速增强 参数。",
          "min": 0,
          "max": 200,
          "step": 5
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "加速度限制"
        },
        {
          "type": "text",
          "param": "CruiseMaxVals0",
          "label": "巡航最大加速度 0",
          "desc": "巡航最大加速度 0 参数。"
        },
        {
          "type": "text",
          "param": "CruiseMaxVals1",
          "label": "巡航最大加速度 1",
          "desc": "巡航最大加速度 1 参数。"
        },
        {
          "type": "text",
          "param": "CruiseMaxVals2",
          "label": "巡航最大加速度 2",
          "desc": "巡航最大加速度 2 参数。"
        },
        {
          "type": "text",
          "param": "CruiseMaxVals3",
          "label": "巡航最大加速度 3",
          "desc": "巡航最大加速度 3 参数。"
        },
        {
          "type": "text",
          "param": "CruiseMaxVals4",
          "label": "巡航最大加速度 4",
          "desc": "巡航最大加速度 4 参数。"
        },
        {
          "type": "text",
          "param": "CruiseMaxVals5",
          "label": "巡航最大加速度 5",
          "desc": "巡航最大加速度 5 参数。"
        },
        {
          "type": "text",
          "param": "CruiseMaxVals6",
          "label": "巡航最大加速度 6",
          "desc": "巡航最大加速度 6 参数。"
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "巡航行为"
        },
        {
          "type": "int",
          "param": "CarrotCruiseDecel",
          "label": "Carrot 巡航减速强度",
          "desc": "Carrot 巡航减速强度 参数。",
          "min": -100,
          "max": 0,
          "step": 1
        },
        {
          "type": "int",
          "param": "CarrotCruiseAtcDecel",
          "label": "Carrot 巡航 ATC 减速强度",
          "desc": "Carrot 巡航 ATC 减速强度 参数。",
          "min": -100,
          "max": 0,
          "step": 1
        },
        {
          "type": "int",
          "param": "VEgoStopping",
          "label": "停车判定车速",
          "desc": "停车判定车速 参数。",
          "min": 0,
          "max": 500,
          "step": 5
        },
        {
          "type": "int",
          "param": "ApplyModelSpeed",
          "label": "模型速度补偿",
          "desc": "模型速度补偿 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
      ]},
      {"type": "tab", "tab": "导航", "widgets": [
        {
          "type": "section",
          "label": "导航限速控制"
        },
        {
          "type": "int",
          "param": "AutoNaviSpeedCtrlMode",
          "label": "导航限速控制模式",
          "desc": "导航限速控制模式 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoNaviSpeedDecelRate",
          "label": "导航限速减速率",
          "desc": "导航限速减速率 参数。",
          "min": 0,
          "max": 500,
          "step": 10
        },
        {
          "type": "int",
          "param": "AutoNaviSpeedSafetyFactor",
          "label": "导航限速安全余量",
          "desc": "导航限速安全余量 参数。",
          "min": 50,
          "max": 150,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoNaviSpeedCtrlEnd",
          "label": "导航限速控制结束距离",
          "desc": "导航限速控制结束距离 参数。",
          "min": 0,
          "max": 30,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "停车 / 测速相机"
        },
        {
          "type": "int",
          "param": "StopDistanceCarrot",
          "label": "停车目标距离",
          "desc": "停车目标距离 参数。",
          "min": 0,
          "max": 2000,
          "step": 10
        },
        {
          "type": "bool",
          "param": "SameSpiCamFilter",
          "label": "同方向测速相机过滤",
          "desc": "同方向测速相机过滤 参数。",
          "default": True
        },
        {
          "type": "int",
          "param": "HapticFeedbackWhenSpeedCamera",
          "label": "测速相机震动提醒",
          "desc": "测速相机震动提醒 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "int",
          "param": "TrafficStopDistanceAdjust",
          "label": "红绿灯停车距离修正",
          "desc": "红绿灯停车距离修正 参数。",
          "min": -500,
          "max": 500,
          "step": 10
        },
        {
          "type": "int",
          "param": "TrafficLightDetectMode",
          "label": "红绿灯检测模式",
          "desc": "红绿灯检测模式 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "道路限速"
        },
        {
          "type": "int",
          "param": "AutoRoadSpeedAdjust",
          "label": "道路限速自动修正",
          "desc": "道路限速自动修正 参数。",
          "min": -50,
          "max": 50,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoRoadSpeedLimitOffset",
          "label": "道路限速偏移量",
          "desc": "道路限速偏移量 参数。",
          "min": -30,
          "max": 30,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoSpeedUptoRoadSpeedLimit",
          "label": "自动提速至道路限速",
          "desc": "自动提速至道路限速 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "int",
          "param": "SpeedFromPCM",
          "label": "车速来源 PCM",
          "desc": "车速来源 PCM 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "int",
          "param": "RoadType",
          "label": "道路类型",
          "desc": "道路类型 参数。",
          "min": -1,
          "max": 5,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Vehicle CAN Speed Arbitration"
        },
        {
          "type": "multiple_button",
          "param": "VehicleNaviCanControl",
          "label": "车辆导航 CAN 控制",
          "desc": "车辆导航 CAN 控制 参数。",
          "buttons": ["Off", "Camera/Bump Always", "Camera Always/Bump Route", "Camera/Bump Route"],
          "visible_if": {
            "param": "CarrotEnabled",
            "eq": "1"
          }
        },
        {
          "type": "bool",
          "param": "VehicleNaviSchoolZoneControl",
          "label": "学校区域 CAN 控制",
          "desc": "学校区域 CAN 控制 参数。",
          "visible_if": {
            "param": "CarrotEnabled",
            "eq": "1"
          },
          "default": False
        },
        {
          "type": "multiple_button",
          "param": "VehicleSpeedCameraControlMode",
          "label": "测速相机控制模式",
          "desc": "测速相机控制模式 参数。",
          "buttons": ["Off", "Always Apply", "Gas Floor", "Gas Pause"],
          "visible_if": {
            "param": "CarrotEnabled",
            "eq": "1"
          }
        },
        {
          "type": "int",
          "param": "VehicleSpeedCameraDistanceTime",
          "label": "测速相机提前提醒时间",
          "desc": "测速相机提前提醒时间 参数。",
          "min": 10,
          "max": 200,
          "step": 1,
          "visible_if": {
            "param": "CarrotEnabled",
            "eq": "1"
          }
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Speed Bumps"
        },
        {
          "type": "int",
          "param": "AutoNaviSpeedBumpEndDistance",
          "label": "减速带结束距离",
          "desc": "减速带结束距离 参数。",
          "min": 0,
          "max": 5000,
          "step": 10,
          "visible_if": {
            "param": "CarrotEnabled",
            "eq": "1"
          }
        },
        {
          "type": "int",
          "param": "AutoNaviCountDownMode",
          "label": "倒计时模式",
          "desc": "倒计时模式 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoNaviSpeedBumpSpeed",
          "label": "减速带目标速度",
          "desc": "减速带目标速度 参数。",
          "min": 0,
          "max": 100,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoNaviSpeedBumpTime",
          "label": "减速带保持时间",
          "desc": "减速带保持时间 参数。",
          "min": 0,
          "max": 10,
          "step": 1
        },
      ]},
      {"type": "tab", "tab": "速度", "widgets": [
        {
          "type": "section",
          "label": "ATC Turn Control"
        },
        {
          "type": "int",
          "param": "AutoTurnControl",
          "label": "自动转向控制",
          "desc": "自动转向控制 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoTurnControlSpeedTurn",
          "label": "自动转向车速阈值",
          "desc": "自动转向车速阈值 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoTurnControlTurnEnd",
          "label": "自动转向结束距离",
          "desc": "自动转向结束距离 参数。",
          "min": 0,
          "max": 50,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoTurnMapChange",
          "label": "导航变道时自动转向",
          "desc": "导航变道时自动转向 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoTurnDistOffset",
          "label": "自动转向距离偏移",
          "desc": "自动转向距离偏移 参数。",
          "min": 0,
          "max": 1000,
          "step": 5
        },
        {
          "type": "bool",
          "param": "AutoTurnInNotRoadEdge",
          "label": "非路沿处允许自动转向",
          "desc": "非路沿处允许自动转向 参数。",
          "default": True
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Fork Control"
        },
        {
          "type": "int",
          "param": "AutoForkDistOffset",
          "label": "匝道汇入距离偏移",
          "desc": "匝道汇入距离偏移 参数。",
          "min": 0,
          "max": 500,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoForkDistOffsetH",
          "label": "匝道汇入距离偏移（高速）",
          "desc": "匝道汇入距离偏移（高速） 参数。",
          "min": 0,
          "max": 2000,
          "step": 10
        },
        {
          "type": "int",
          "param": "AutoDoForkBlinkerDist",
          "label": "匝道转向灯触发距离",
          "desc": "匝道转向灯触发距离 参数。",
          "min": 0,
          "max": 200,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoDoForkBlinkerDistH",
          "label": "匝道转向灯触发距离（高速）",
          "desc": "匝道转向灯触发距离（高速） 参数。",
          "min": 0,
          "max": 500,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoDoForkNavDist",
          "label": "导航匝道触发距离",
          "desc": "导航匝道触发距离 参数。",
          "min": 0,
          "max": 200,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoDoForkNavDistH",
          "label": "导航匝道触发距离（高速）",
          "desc": "导航匝道触发距离（高速） 参数。",
          "min": 0,
          "max": 500,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoDoForkDecalDist",
          "label": "匝道减速触发距离",
          "desc": "匝道减速触发距离 参数。",
          "min": 0,
          "max": 300,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoDoForkDecalDistH",
          "label": "匝道减速触发距离（高速）",
          "desc": "匝道减速触发距离（高速） 参数。",
          "min": 0,
          "max": 500,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoForkDecalRate",
          "label": "匝道减速率",
          "desc": "匝道减速率 参数。",
          "min": 0,
          "max": 500,
          "step": 10
        },
        {
          "type": "int",
          "param": "AutoForkDecalRateH",
          "label": "匝道减速率（高速）",
          "desc": "匝道减速率（高速） 参数。",
          "min": 0,
          "max": 500,
          "step": 10
        },
        {
          "type": "int",
          "param": "AutoForkSpeedMin",
          "label": "匝道最低速度",
          "desc": "匝道最低速度 参数。",
          "min": 0,
          "max": 120,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoForkSpeedMinH",
          "label": "匝道最低速度（高速）",
          "desc": "匝道最低速度（高速） 参数。",
          "min": 0,
          "max": 120,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoKeepForkSpeed",
          "label": "匝道保持速度",
          "desc": "匝道保持速度 参数。",
          "min": 0,
          "max": 60,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoKeepForkSpeedH",
          "label": "匝道保持速度（高速）",
          "desc": "匝道保持速度（高速） 参数。",
          "min": 0,
          "max": 60,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Turn Speed"
        },
        {
          "type": "int",
          "param": "MapTurnSpeedFactor",
          "label": "地图弯道速度系数",
          "desc": "地图弯道速度系数 参数。",
          "min": 0,
          "max": 200,
          "step": 5
        },
        {
          "type": "int",
          "param": "TurnSpeedControlMode",
          "label": "弯道速度控制模式",
          "desc": "弯道速度控制模式 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "弯道限速"
        },
        {
          "type": "int",
          "param": "AutoCurveSpeedFactor",
          "label": "弯道限速系数",
          "desc": "弯道限速系数 参数。",
          "min": 10,
          "max": 200,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoCurveSpeedFactorH",
          "label": "弯道限速系数（高速）",
          "desc": "弯道限速系数（高速） 参数。",
          "min": 10,
          "max": 200,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoCurveSpeedAggressivenessH",
          "label": "高速弯道激进程度",
          "desc": "高速弯道激进程度 参数。",
          "min": 10,
          "max": 200,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoCurveSpeedLowerLimit",
          "label": "弯道限速下限",
          "desc": "弯道限速下限 参数。",
          "min": 0,
          "max": 150,
          "step": 5
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Road Limit Raising"
        },
        {
          "type": "int",
          "param": "AutoUpRoadLimit",
          "label": "自动提升道路限速",
          "desc": "自动提升道路限速 参数。",
          "min": 0,
          "max": 120,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoUpRoadLimit40KMH",
          "label": "40 km/h 限速自动提升",
          "desc": "40 km/h 限速自动提升 参数。",
          "min": 0,
          "max": 60,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoUpHighwayRoadLimit",
          "label": "高速公路限速自动提升",
          "desc": "高速公路限速自动提升 参数。",
          "min": 0,
          "max": 160,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoUpHighwayRoadLimit40KMH",
          "label": "高速 40 km/h 限速自动提升",
          "desc": "高速 40 km/h 限速自动提升 参数。",
          "min": 0,
          "max": 60,
          "step": 1
        },
      ]},
      {"type": "tab", "tab": "调节", "widgets": [
        {
          "type": "section",
          "label": "Lateral Mode"
        },
        {
          "type": "int",
          "param": "AlwaysLateral",
          "label": "始终启用横向控制",
          "desc": "始终启用横向控制 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Steering Limits"
        },
        {
          "type": "int",
          "param": "CustomSR",
          "label": "自定义转向比",
          "desc": "自定义转向比 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "CustomSteerMax",
          "label": "自定义最大转向角",
          "desc": "自定义最大转向角 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "CustomSteerDeltaDown",
          "label": "转向变化率下限",
          "desc": "转向变化率下限 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "CustomSteerDeltaUp",
          "label": "转向变化率上限",
          "desc": "转向变化率上限 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "CustomSteerDeltaDownLC",
          "label": "变道转向变化率下限",
          "desc": "变道转向变化率下限 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "CustomSteerDeltaUpLC",
          "label": "变道转向变化率上限",
          "desc": "变道转向变化率上限 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "SteerActuatorDelay",
          "label": "转向执行器延迟",
          "desc": "转向执行器延迟 参数。",
          "min": 0,
          "max": 200,
          "step": 5
        },
        {
          "type": "int",
          "param": "SteerRatioRate",
          "label": "转向比变化率",
          "desc": "转向比变化率 参数。",
          "min": 0,
          "max": 300,
          "step": 5
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Path Offset"
        },
        {
          "type": "int",
          "param": "PathOffset",
          "label": "路径偏移",
          "desc": "路径偏移 参数。",
          "min": -100,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "AdjustLaneOffset",
          "label": "车道偏移调整",
          "desc": "车道偏移调整 参数。",
          "min": -50,
          "max": 50,
          "step": 1
        },
        {
          "type": "int",
          "param": "CameraYawTrimDeg",
          "label": "相机偏航修正",
          "desc": "相机偏航修正 参数。",
          "min": -20,
          "max": 20,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Lateral MPC Costs"
        },
        {
          "type": "int",
          "param": "LatMpcAccelCost",
          "label": "横向加速度代价",
          "desc": "横向加速度代价 参数。",
          "min": 0,
          "max": 500,
          "step": 5
        },
        {
          "type": "int",
          "param": "LatMpcJerkCost",
          "label": "横向急动度代价",
          "desc": "横向急动度代价 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "LatMpcMotionCost",
          "label": "横向运动代价",
          "desc": "横向运动代价 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "LatMpcPathCost",
          "label": "横向路径代价",
          "desc": "横向路径代价 参数。",
          "min": 0,
          "max": 1000,
          "step": 5
        },
        {
          "type": "int",
          "param": "LatMpcSteeringRateCost",
          "label": "横向转向速率代价",
          "desc": "横向转向速率代价 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Lateral Torque"
        },
        {
          "type": "int",
          "param": "LateralTorqueCustom",
          "label": "自定义横向扭矩",
          "desc": "自定义横向扭矩 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "int",
          "param": "LateralTorqueFriction",
          "label": "横向扭矩摩擦系数",
          "desc": "横向扭矩摩擦系数 参数。",
          "min": 0,
          "max": 300,
          "step": 5
        },
        {
          "type": "int",
          "param": "LateralTorqueKd",
          "label": "横向扭矩微分系数",
          "desc": "横向扭矩微分系数 参数。",
          "min": 0,
          "max": 300,
          "step": 5
        },
        {
          "type": "int",
          "param": "LateralTorqueKf",
          "label": "横向扭矩前馈系数",
          "desc": "横向扭矩前馈系数 参数。",
          "min": 0,
          "max": 300,
          "step": 5
        },
        {
          "type": "int",
          "param": "LateralTorqueKiV",
          "label": "横向扭矩积分速度系数",
          "desc": "横向扭矩积分速度系数 参数。",
          "min": 0,
          "max": 300,
          "step": 5
        },
        {
          "type": "int",
          "param": "LateralTorqueKpV",
          "label": "横向扭矩比例速度系数",
          "desc": "横向扭矩比例速度系数 参数。",
          "min": 0,
          "max": 300,
          "step": 5
        },
        {
          "type": "int",
          "param": "LateralTorqueAccelFactor",
          "label": "横向扭矩加速度系数",
          "desc": "横向扭矩加速度系数 参数。",
          "min": 0,
          "max": 5000,
          "step": 50
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Lateral Smoothing"
        },
        {
          "type": "int",
          "param": "LatMpcInputOffset",
          "label": "横向输入偏移",
          "desc": "横向输入偏移 参数。",
          "min": 0,
          "max": 20,
          "step": 1
        },
        {
          "type": "int",
          "param": "LatSmoothSec",
          "label": "横向平滑时间",
          "desc": "横向平滑时间 参数。",
          "min": 0,
          "max": 50,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "变道"
        },
        {
          "type": "int",
          "param": "LaneChangeBsd",
          "label": "变道盲区检测",
          "desc": "变道盲区检测 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "int",
          "param": "LaneChangeDelay",
          "label": "变道延迟",
          "desc": "变道延迟 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "LaneChangeNeedTorque",
          "label": "变道需要手力",
          "desc": "变道需要手力 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "bool",
          "param": "ContinuousLaneChange",
          "label": "连续变道",
          "desc": "连续变道 参数。",
          "default": True
        },
        {
          "type": "int",
          "param": "ContinuousLaneChangeCnt",
          "label": "连续变道次数",
          "desc": "连续变道次数 参数。",
          "min": 1,
          "max": 10,
          "step": 1
        },
        {
          "type": "int",
          "param": "ContinuousLaneChangeInterval",
          "label": "连续变道间隔",
          "desc": "连续变道间隔 参数。",
          "min": 0,
          "max": 30,
          "step": 1
        },
        {
          "type": "int",
          "param": "AChangeCostStarting",
          "label": "变道起步代价",
          "desc": "变道起步代价 参数。",
          "min": 0,
          "max": 50,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Auto Turn / New Lane"
        },
        {
          "type": "int",
          "param": "LaneStabTime",
          "label": "车道稳定时间",
          "desc": "车道稳定时间 参数。",
          "min": 0,
          "max": 200,
          "step": 10
        },
        {
          "type": "int",
          "param": "NewLaneWidthDiff",
          "label": "新车道宽度差阈值",
          "desc": "新车道宽度差阈值 参数。",
          "min": 0,
          "max": 50,
          "step": 1
        },
        {
          "type": "int",
          "param": "AutoEnTurnNewLaneTime",
          "label": "自动进入新车道时间",
          "desc": "自动进入新车道时间 参数。",
          "min": 0,
          "max": 60,
          "step": 5
        },
        {
          "type": "int",
          "param": "AutoEnTurnNewLaneTimeH",
          "label": "自动进入新车道时间（高速）",
          "desc": "自动进入新车道时间（高速） 参数。",
          "min": 0,
          "max": 60,
          "step": 5
        },
        {
          "type": "bool",
          "param": "AutoTurnLeft",
          "label": "自动左转",
          "desc": "自动左转 参数。",
          "default": True
        },
        {
          "type": "bool",
          "param": "StockBlinkerCtrl",
          "label": "原车转向灯控制",
          "desc": "原车转向灯控制 参数。",
          "default": False
        },
        {
          "type": "bool",
          "param": "ExtBlinkerCtrlTest",
          "label": "扩展转向灯测试",
          "desc": "扩展转向灯测试 参数。",
          "default": False
        },
        {
          "type": "int",
          "param": "BlinkerMode",
          "label": "转向灯模式",
          "desc": "转向灯模式 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "盲区检测"
        },
        {
          "type": "bool",
          "param": "DisableBlindSpot",
          "label": "禁用盲区检测",
          "desc": "禁用盲区检测 参数。",
          "default": False
        },
        {
          "type": "int",
          "param": "DynamicBlindRange",
          "label": "动态盲区范围",
          "desc": "动态盲区范围 参数。",
          "min": 0,
          "max": 100,
          "step": 5
        },
        {
          "type": "int",
          "param": "DynamicBlindDistance",
          "label": "动态盲区距离",
          "desc": "动态盲区距离 参数。",
          "min": 0,
          "max": 100,
          "step": 5
        },
        {
          "type": "int",
          "param": "BsdDelayTime",
          "label": "盲区检测延迟",
          "desc": "盲区检测延迟 参数。",
          "min": 0,
          "max": 100,
          "step": 5
        },
        {
          "type": "int",
          "param": "SideBsdDelayTime",
          "label": "侧向盲区延迟",
          "desc": "侧向盲区延迟 参数。",
          "min": 0,
          "max": 100,
          "step": 5
        },
        {
          "type": "int",
          "param": "SideRelDistTime",
          "label": "侧向相对距离时间",
          "desc": "侧向相对距离时间 参数。",
          "min": 0,
          "max": 100,
          "step": 5
        },
        {
          "type": "int",
          "param": "SidevRelDistTime",
          "label": "侧向相对速度时间",
          "desc": "侧向相对速度时间 参数。",
          "min": 0,
          "max": 100,
          "step": 5
        },
        {
          "type": "int",
          "param": "SideRadarMinDist",
          "label": "侧向雷达最小距离",
          "desc": "侧向雷达最小距离 参数。",
          "min": 0,
          "max": 50,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Lane Line / ONNX"
        },
        {
          "type": "int",
          "param": "LaneLineCheck",
          "label": "车道线检查",
          "desc": "车道线检查 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "int",
          "param": "OnnxBsdIntervalMs",
          "label": "ONNX 盲区检测间隔",
          "desc": "ONNX 盲区检测间隔 参数。",
          "min": 50,
          "max": 1000,
          "step": 10
        },
        {
          "type": "int",
          "param": "OnnxBsdSmoothingMs",
          "label": "ONNX 盲区检测平滑",
          "desc": "ONNX 盲区检测平滑 参数。",
          "min": 0,
          "max": 1000,
          "step": 10
        },
        {
          "type": "int",
          "param": "OnnxBsdThreshold",
          "label": "ONNX 盲区检测阈值",
          "desc": "ONNX 盲区检测阈值 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
        {
          "type": "int",
          "param": "OnnxLaneIntervalMs",
          "label": "ONNX 车道检测间隔",
          "desc": "ONNX 车道检测间隔 参数。",
          "min": 50,
          "max": 1000,
          "step": 10
        },
        {
          "type": "int",
          "param": "OnnxLaneThreshold",
          "label": "ONNX 车道检测阈值",
          "desc": "ONNX 车道检测阈值 参数。",
          "min": 0,
          "max": 100,
          "step": 1
        },
      ]},
      {"type": "tab", "tab": "显示", "widgets": [
        {
          "type": "section",
          "label": "Steering Suspend"
        },
        {
          "type": "int",
          "param": "LatSuspendAngleDeg",
          "label": "横向挂起角度",
          "desc": "横向挂起角度 参数。",
          "min": 45,
          "max": 300,
          "step": 10
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Cluster Map"
        },
        {
          "type": "multiple_button",
          "param": "ClusterNaviMapTheme",
          "label": "仪表导航地图主题",
          "desc": "仪表导航地图主题 参数。",
          "buttons": ["Auto", "Dark", "Light"],
          "visible_if": {
            "param": "CarrotEnabled",
            "eq": "1"
          }
        },
        {
          "type": "multiple_button",
          "param": "ClusterNaviMapType",
          "label": "仪表导航地图类型",
          "desc": "仪表导航地图类型 参数。",
          "buttons": ["Normal", "Satellite"],
          "visible_if": {
            "param": "CarrotEnabled",
            "eq": "1"
          }
        },
        {
          "type": "multiple_button",
          "param": "ClusterNaviMapFps",
          "label": "仪表导航地图帧率",
          "desc": "仪表导航地图帧率 参数。",
          "buttons": ["5 FPS", "10 FPS", "20 FPS", "30 FPS"],
          "visible_if": {
            "param": "CarrotEnabled",
            "eq": "1"
          }
        },
        {
          "type": "bool",
          "param": "CarrotNaviHudMapProfile",
          "label": "Carrot HUD 地图配置",
          "desc": "Carrot HUD 地图配置 参数。",
          "visible_if": {
            "param": "CarrotEnabled",
            "eq": "1"
          },
          "default": False
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Cluster HUD"
        },
        {
          "type": "bool",
          "param": "ClusterHud",
          "label": "仪表 HUD",
          "desc": "仪表 HUD 参数。",
          "default": 0
        },
        {
          "type": "int",
          "param": "ClusterHudBrightness",
          "label": "仪表 HUD 亮度",
          "desc": "仪表 HUD 亮度 参数。",
          "min": 0,
          "max": 100,
          "step": 5
        },
        {
          "type": "int",
          "param": "ClusterHudCameraViewMode",
          "label": "仪表 HUD 相机视图模式",
          "desc": "仪表 HUD 相机视图模式 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "int",
          "param": "ClusterHudCoreMode",
          "label": "仪表 HUD 核心模式",
          "desc": "仪表 HUD 核心模式 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "bool",
          "param": "ClusterHudDebug",
          "label": "仪表 HUD 调试",
          "desc": "仪表 HUD 调试 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "ClusterHudEncoder",
          "label": "仪表 HUD 编码器",
          "desc": "仪表 HUD 编码器 参数。",
          "default": 0
        },
        {
          "type": "int",
          "param": "ClusterHudLiveFps",
          "label": "仪表 HUD 实时帧率",
          "desc": "仪表 HUD 实时帧率 参数。",
          "min": 1,
          "max": 60,
          "step": 1
        },
        {
          "type": "bool",
          "param": "ClusterHudMirror",
          "label": "仪表 HUD 镜像",
          "desc": "仪表 HUD 镜像 参数。",
          "default": 0
        },
        {
          "type": "int",
          "param": "ClusterHudOrientation",
          "label": "仪表 HUD 方向",
          "desc": "仪表 HUD 方向 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "int",
          "param": "ClusterHudPanelLayout",
          "label": "仪表 HUD 面板布局",
          "desc": "仪表 HUD 面板布局 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "int",
          "param": "ClusterHudPriority",
          "label": "仪表 HUD 优先级",
          "desc": "仪表 HUD 优先级 参数。",
          "min": 0,
          "max": 20,
          "step": 1
        },
        {
          "type": "bool",
          "param": "ClusterHudRadarDisplay",
          "label": "仪表 HUD 雷达显示",
          "desc": "仪表 HUD 雷达显示 参数。",
          "default": 0
        },
        {
          "type": "int",
          "param": "ClusterHudRadarInfo",
          "label": "仪表 HUD 雷达信息",
          "desc": "仪表 HUD 雷达信息 参数。",
          "min": 0,
          "max": 10,
          "step": 1
        },
        {
          "type": "bool",
          "param": "ClusterHudRadarSourceColor",
          "label": "仪表 HUD 雷达颜色源",
          "desc": "仪表 HUD 雷达颜色源 参数。",
          "default": 0
        },
        {
          "type": "int",
          "param": "ClusterHudScreenMode",
          "label": "仪表 HUD 屏幕模式",
          "desc": "仪表 HUD 屏幕模式 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "int",
          "param": "ClusterHudTheme",
          "label": "仪表 HUD 主题",
          "desc": "仪表 HUD 主题 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "On-Screen Info"
        },
        {
          "type": "bool",
          "param": "ShowCameraWithCluster",
          "label": "仪表显示摄像头",
          "desc": "仪表显示摄像头 参数。",
          "default": 0
        },
        {
          "type": "int",
          "param": "ShowCustomBrightness",
          "label": "自定义亮度显示",
          "desc": "自定义亮度显示 参数。",
          "min": 0,
          "max": 100,
          "step": 5
        },
        {
          "type": "bool",
          "param": "ShowDateTime",
          "label": "显示日期时间",
          "desc": "显示日期时间 参数。",
          "default": 1
        },
        {
          "type": "bool",
          "param": "ShowDebugUI",
          "label": "显示调试界面",
          "desc": "显示调试界面 参数。",
          "default": 1
        },
        {
          "type": "bool",
          "param": "ShowDeviceState",
          "label": "显示设备状态",
          "desc": "显示设备状态 参数。",
          "default": 1
        },
        {
          "type": "bool",
          "param": "ShowLaneInfo",
          "label": "显示车道信息",
          "desc": "显示车道信息 参数。",
          "default": 1
        },
        {
          "type": "bool",
          "param": "ShowModelView",
          "label": "显示模型视图",
          "desc": "显示模型视图 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "ShowPlotMode",
          "label": "显示绘图模式",
          "desc": "显示绘图模式 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "ShowRadarInfo",
          "label": "显示雷达信息",
          "desc": "显示雷达信息 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "ShowRouteInfo",
          "label": "显示路线信息",
          "desc": "显示路线信息 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "ShowTpms",
          "label": "显示胎压",
          "desc": "显示胎压 参数。",
          "default": 1
        },
        {
          "type": "bool",
          "param": "SoftwareMenu",
          "label": "软件菜单",
          "desc": "软件菜单 参数。",
          "default": 0
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Sound / Map"
        },
        {
          "type": "int",
          "param": "SoundVolumeAdjust",
          "label": "提示音音量调整",
          "desc": "提示音音量调整 参数。",
          "min": 0,
          "max": 200,
          "step": 10
        },
        {
          "type": "int",
          "param": "SoundVolumeAdjustEngage",
          "label": "激活提示音音量",
          "desc": "激活提示音音量 参数。",
          "min": 0,
          "max": 200,
          "step": 10
        },
        {
          "type": "text",
          "param": "SoundLanguageSetting",
          "label": "提示音语言",
          "desc": "提示音语言 参数。"
        },
        {
          "type": "int",
          "param": "MapboxStyle",
          "label": "Mapbox 地图样式",
          "desc": "Mapbox 地图样式 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "YouTube Live"
        },
        {
          "type": "bool",
          "param": "CarrotYouTubeLive",
          "label": "Carrot YouTube 直播",
          "desc": "Carrot YouTube 直播 参数。",
          "default": 0
        },
        {
          "type": "int",
          "param": "CarrotYouTubeQuality",
          "label": "Carrot YouTube 画质",
          "desc": "Carrot YouTube 画质 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "bool",
          "param": "CarrotYouTubeTimestamp",
          "label": "Carrot YouTube 时间戳",
          "desc": "Carrot YouTube 时间戳 参数。",
          "default": 0
        },
      ]},
      {"type": "tab", "tab": "轨迹", "widgets": [
        {
          "type": "section",
          "label": "Path Appearance"
        },
        {
          "type": "int",
          "param": "ShowPathColor",
          "label": "路径颜色",
          "desc": "路径颜色 参数。",
          "min": 0,
          "max": 20,
          "step": 1
        },
        {
          "type": "int",
          "param": "ShowPathColorCruiseOff",
          "label": "未巡航路径颜色",
          "desc": "未巡航路径颜色 参数。",
          "min": 0,
          "max": 20,
          "step": 1
        },
        {
          "type": "int",
          "param": "ShowPathColorLane",
          "label": "车道路径颜色",
          "desc": "车道路径颜色 参数。",
          "min": 0,
          "max": 20,
          "step": 1
        },
        {
          "type": "bool",
          "param": "ShowPathEnd",
          "label": "路径终点显示",
          "desc": "路径终点显示 参数。",
          "default": 1
        },
        {
          "type": "int",
          "param": "ShowPathMode",
          "label": "路径显示模式",
          "desc": "路径显示模式 参数。",
          "min": 0,
          "max": 20,
          "step": 1
        },
        {
          "type": "int",
          "param": "ShowPathModeLane",
          "label": "车道路径显示模式",
          "desc": "车道路径显示模式 参数。",
          "min": 0,
          "max": 20,
          "step": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Trajectory / Lane Line"
        },
        {
          "type": "bool",
          "param": "CarrotTireTrajectory",
          "label": "轮胎轨迹",
          "desc": "轮胎轨迹 参数。",
          "default": 0
        },
        {
          "type": "int",
          "param": "UseLaneLineCurveSpeed",
          "label": "使用车道线弯道限速",
          "desc": "使用车道线弯道限速 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
        {
          "type": "int",
          "param": "UseLaneLineSpeed",
          "label": "使用车道线速度",
          "desc": "使用车道线速度 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
      ]},
      {"type": "tab", "tab": "车辆", "widgets": [
        {
          "type": "section",
          "label": "Driver / Safety"
        },
        {
          "type": "bool",
          "param": "DisableDM",
          "label": "禁用驾驶员监控",
          "desc": "禁用驾驶员监控 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "DisableMinSteerSpeed",
          "label": "禁用最低转向速度",
          "desc": "禁用最低转向速度 参数。",
          "default": 0
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Vehicle Features"
        },
        {
          "type": "bool",
          "param": "HyundaiCameraSCC",
          "label": "现代摄像头自适应巡航",
          "desc": "现代摄像头自适应巡航 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "IsLdwsCar",
          "label": "车道偏离预警车辆",
          "desc": "车道偏离预警车辆 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "HDPuse",
          "label": "HDP 使用",
          "desc": "HDP 使用 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "HotspotOnBoot",
          "label": "开机启动热点",
          "desc": "开机启动热点 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "UseWideCamera",
          "label": "使用广角摄像头",
          "desc": "使用广角摄像头 参数。",
          "default": 1
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Radar / Tracks"
        },
        {
          "type": "bool",
          "param": "EnableCornerRadar",
          "label": "启用角雷达",
          "desc": "启用角雷达 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "EnableRadarTracks",
          "label": "启用雷达跟踪",
          "desc": "启用雷达跟踪 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "EnableSpeedTF",
          "label": "启用速度 TF",
          "desc": "启用速度 TF 参数。",
          "default": 0
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Comfort"
        },
        {
          "type": "bool",
          "param": "MuteDoor",
          "label": "静音车门",
          "desc": "静音车门 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "MuteSeatbelt",
          "label": "静音安全带",
          "desc": "静音安全带 参数。",
          "default": 0
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Driving Data"
        },
        {
          "type": "bool",
          "param": "RecordRoadCam",
          "label": "录制道路摄像头",
          "desc": "录制道路摄像头 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "ShareData",
          "label": "共享数据",
          "desc": "共享数据 参数。",
          "default": 0
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Timeouts"
        },
        {
          "type": "int",
          "param": "MaxAngleFrames",
          "label": "最大角度帧数",
          "desc": "最大角度帧数 参数。",
          "min": 0,
          "max": 200,
          "step": 1
        },
        {
          "type": "int",
          "param": "MaxTimeOffroadMin",
          "label": "Max Time Offroad (min)",
          "desc": "Maximum offroad time before shutdown (minutes). Default 60.",
          "min": 0,
          "max": 600,
          "step": 5
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Driving Mode"
        },
        {
          "type": "int",
          "param": "MyDrivingMode",
          "label": "我的驾驶模式",
          "desc": "我的驾驶模式 参数。",
          "min": 0,
          "max": 3,
          "step": 1
        },
        {
          "type": "int",
          "param": "MyDrivingModeAuto",
          "label": "我的驾驶模式自动",
          "desc": "我的驾驶模式自动 参数。",
          "min": 0,
          "max": 2,
          "step": 1
        },
      ]},
      {"type": "tab", "tab": "开发者", "widgets": [
        {
          "type": "section",
          "label": "CAN-FD Debug"
        },
        {
          "type": "bool",
          "param": "CanfdDebug",
          "label": "CANFD 调试",
          "desc": "CANFD 调试 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "CanfdHDA2",
          "label": "CANFD HDA2",
          "desc": "CANFD HDA2 参数。",
          "default": 0
        },
        {
          "type": "separator"
        },
        {
          "type": "section",
          "label": "Hardware / Tests"
        },
        {
          "type": "bool",
          "param": "HardwareC3xLite",
          "label": "C3X Lite 硬件",
          "desc": "C3X Lite 硬件 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "CruiseButtonTest1",
          "label": "巡航按钮测试 1",
          "desc": "巡航按钮测试 1 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "CruiseButtonTest2",
          "label": "巡航按钮测试 2",
          "desc": "巡航按钮测试 2 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "CruiseButtonTest3",
          "label": "巡航按钮测试 3",
          "desc": "巡航按钮测试 3 参数。",
          "default": 0
        },
        {
          "type": "bool",
          "param": "ShowDebugLog",
          "label": "显示调试日志",
          "desc": "显示调试日志 参数。",
          "default": False
        },
      ]},
      {
        "type": "separator"
      },
      {
        "type": "action",
        "label": "Reset Carrot Tuning",
        "desc": "Restore every Carrot tuning parameter on this page to its compiled-in default.",
        "action": "carrot_tuning_reset",
        "confirm": "Reset all Carrot tuning parameters to defaults?",
        "button": "RESET"
      },
    ],
  },

  "steering__mads": {
    "id": "steering__mads",
    "title": "Customize MADS",
    "parent": "steering",
    "widgets": [
      {"type": "bool", "param": "MadsMainCruiseAllowed", "label": "Toggle with Main Cruise"},
      {"type": "bool", "param": "MadsUnifiedEngagementMode", "label": "Unified Engagement Mode (UEM)"},
      {"type": "multiple_button", "param": "MadsSteeringMode", "label": "Steering Mode on Brake Pedal",
       "buttons": ["Remain Active", "Pause", "Disengage"]},
    ],
  },
  "steering__lane_change": {
    "id": "steering__lane_change",
    "title": "Customize Lane Change",
    "parent": "steering",
    "widgets": [
      {"type": "option", "param": "AutoLaneChangeTimer", "label": "Auto Lane Change by Blinker",
       "min": -1, "max": 5, "step": 1, "label_format": "lane_change_timer", "layout": "stacked",
       "desc": "Set a timer to delay the auto lane change operation when the blinker is used. "
               "No nudge on the steering wheel is required to auto lane change if a timer is set. Default is Nudge. "
               "Please use caution when using this feature. Only use the blinker when traffic and road conditions permit."},
      {"type": "separator"},
      {"type": "bool", "param": "AutoLaneChangeBsmDelay", "label": "Auto Lane Change: Delay with Blind Spot",
       "desc": "Toggle to enable a delay timer for seamless lane changes when blind spot monitoring (BSM) "
               "detects a obstructing vehicle, ensuring safe maneuvering."},
      {"type": "separator"},
      {"type": "bool", "param": "RoadEdgeLaneChangeEnabled", "label": "Block Lane Change: Road Edge Detection",
       "desc": "Blocks the lane change if the model sees a road edge on your signaled side."},
    ],
  },
  "steering__torque": {
    "id": "steering__torque",
    "title": "Customize Torque Params",
    "parent": "steering",
    "widgets": [
      {"type": "bool", "param": "LateralJerkTorqueController", "label": "Lateral Jerk Torque Controller", "offroad_only": True,
       "desc": "Looks ahead at planned steering to reduce sudden corrections, so the wheel moves more smoothly through turns. Works with Self-Tune and custom tuning. Thanks to @twilsonco for the implementation."},
      {"type": "action", "action": "torque_tune_version", "label": "Torque Control Tune Version", "button": "SELECT",
       "desc": "Select the version of Torque Control Tune to use."},
      {"type": "bool", "param": "LiveTorqueParamsToggle", "label": "Self-Tune", "offroad_only": True,
       "desc": "Enables self-tune for Torque lateral control for platforms that do not use Torque lateral control by default."},
      {"type": "bool", "param": "LiveTorqueParamsRelaxedToggle", "label": "Less Restrict Settings for Self-Tune (Beta)",
       "desc": "Less strict settings when using Self-Tune. This allows torqued to be more forgiving when learning values.",
       "visible_if": {"param": "LiveTorqueParamsToggle", "eq": "1"}, "offroad_only": True},
      {"type": "bool", "param": "CustomTorqueParams", "label": "Enable Custom Tuning", "offroad_only": True,
       "desc": "Enables custom tuning for Torque lateral control. Modifying Lateral Acceleration Factor and Friction below will override the offline values indicated in the YAML files within \"opendbc/car/torque_data\". The values will also be used live when \"Manual Real-Time Tuning\" toggle is enabled."},
      {"type": "bool", "param": "TorqueParamsOverrideEnabled", "label": "Manual Real-Time Tuning",
       "desc": "Enforces the torque lateral controller to use the fixed values instead of the learned values from Self-Tune. Enabling this toggle overrides Self-Tune values.",
       "visible_if": {"param": "CustomTorqueParams", "eq": "1"}, "offroad_only": True},
      {"type": "option", "param": "TorqueParamsOverrideLatAccelFactor", "label": "Lateral Acceleration Factor",
       "min": 1, "max": 500, "step": 1, "label_format": "torque_lat_accel",
       "visible_if": {"param": "CustomTorqueParams", "eq": "1"}},
      {"type": "option", "param": "TorqueParamsOverrideFriction", "label": "Friction",
       "min": 1, "max": 100, "step": 1, "label_format": "torque_friction",
       "visible_if": {"param": "CustomTorqueParams", "eq": "1"}},
    ],
  },
  "cruise__sla": {
    "id": "cruise__sla",
    "title": "Speed Limit",
    "parent": "cruise",
    "widgets": [
      {"type": "multiple_button", "param": "SpeedLimitMode", "label": "Speed Limit",
       "buttons": ["Off", "Info", "Warning", "Assist"]},
      {"type": "custom", "custom": "speed_limit_sources", "label": "Speed Limit Sources",
       "desc": "Real-time values from the car (TSR), map provider (OSM/Amap), and Carrot navigation. The merged value is what the Speed Limit widget currently displays."},
      {"type": "custom", "custom": "longitudinal_source", "label": "Longitudinal Source",
       "desc": "Which longitudinal plan source is currently winning the arbitration: cruise, sccVision, sccMap, speedLimitAssist, or carrot."},
      {"type": "custom", "custom": "traffic_light_fusion", "label": "Traffic Light Fusion",
       "desc": "Fused traffic-light state from Carrot/Amap navigation and vision stop-line detection."},
      {"type": "subpanel", "target": "cruise__sla__policy", "label": "Customize Source", "button": "CUSTOMIZE"},
      {"type": "multiple_button", "param": "SpeedLimitOffsetType", "label": "Speed Limit Offset",
       "buttons": ["None", "Fixed", "%"]},
      {"type": "option", "param": "SpeedLimitValueOffset", "label": "Offset Value",
       "min": -30, "max": 30, "step": 1, "label_format": "speed_limit_offset",
       "visible_if": {"param": "SpeedLimitOffsetType", "ne": "0"}},
    ],
  },
  "cruise__sla__policy": {
    "id": "cruise__sla__policy",
    "title": "Speed Limit Source",
    "parent": "cruise__sla",
    "widgets": [
      {"type": "multiple_button", "param": "SpeedLimitPolicy", "label": "Speed Limit Source",
       "buttons": ["Car Only", "Map Only", "Car First", "Map First", "Combined"]},
    ],
  },
  "network__advanced": {
    "id": "network__advanced",
    "title": "Advanced Network",
    "parent": "network",
    "custom": "network_advanced",
    "widgets": [
      {"type": "bool", "param": "GsmRoaming", "label": "Enable Roaming"},
      {"type": "bool", "param": "GsmMetered", "label": "Cellular Metered",
       "desc": "Prevent large data uploads when on a metered cellular connection"},
    ],
  },
  "cruise__longitudinal_mpc_tuning": {
    "id": "cruise__longitudinal_mpc_tuning",
    "title": "Longitudinal MPC Tuning",
    "parent": "cruise",
    "custom": "longitudinal_mpc_tuning",
    "widgets": [],
  },
}


def panel_ids() -> list[str]:
  return [p["id"] for p in PANELS]


def get_panel(panel_id: str) -> dict[str, Any] | None:
  if panel_id in SUBPANELS:
    return SUBPANELS[panel_id]
  for p in PANELS:
    if p["id"] == panel_id:
      return p
  return None


def panel_schema() -> dict[str, Any]:
  from webui.server.bridge.design_tokens import PANEL_ICONS, tokens_payload
  from webui.server.bridge.headless_util import is_headless_mode
  from webui.server.bridge.lite_util import is_lite_hw, should_hide_widget

  headless = is_headless_mode()
  lite = is_lite_hw()
  headless_hide_params = {
    "Brightness", "OnroadScreenOffBrightness", "OnroadScreenOffTimer",
    "InteractivityTimeout", "ScreenSaverEnabled", "ScreenSaverTimeout",
  }

  def _filter_widgets(widgets: list[dict]) -> list[dict]:
    out = []
    for w in widgets:
      if should_hide_widget(w):
        continue
      if headless and w.get("param") in headless_hide_params:
        continue
      if w.get("type") == "separator" and out and out[-1].get("type") == "separator":
        continue
      out.append(w)
    return out

  panels_out = []
  for p in PANELS:
    entry = {**p, "icon": PANEL_ICONS.get(p["id"], "")}
    widgets = _filter_widgets(list(entry.get("widgets") or []))
    if headless and p.get("id") == "display":
      entry["headless_note"] = "Built-in display settings are hidden on headless devices."
      widgets.insert(0, {
        "type": "html",
        "i18n_key": "No built-in screen — brightness and screen saver do not apply. Camera stream settings below are used by Web UI.",
      })
      widgets.insert(1, {"type": "separator"})
    entry["widgets"] = widgets
    panels_out.append(entry)
  return {
    "ok": True,
    "panels": panels_out,
    "subpanels": list(SUBPANELS.keys()),
    "headless": headless,
    "lite": lite,
    **tokens_payload(),
  }


def _collect_widget_keys(widgets: list[dict], keys: list[str]) -> None:
  for w in widgets:
    for dep_key in ("visible_if", "advanced_if"):
      dep = w.get(dep_key)
      if isinstance(dep, dict) and dep.get("param"):
        keys.append(dep["param"])
    if w.get("type") == "dual_button":
      for side in ("left", "right"):
        sk = (w.get(side) or {}).get("param")
        if sk:
          keys.append(sk)
      continue
    if w.get("type") == "tab" and "widgets" in w:
      _collect_widget_keys(w["widgets"], keys)
      continue
    key = w.get("param")
    if key:
      keys.append(key)


def panel_param_keys(panel_id: str) -> list[str]:
  panel = get_panel(panel_id)
  if not panel:
    return []
  keys: list[str] = []
  _collect_widget_keys(panel.get("widgets", []), keys)
  return sorted(set(keys))

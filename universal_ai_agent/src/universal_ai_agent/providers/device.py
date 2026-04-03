from __future__ import annotations

from typing import Any, Callable


class DeviceActionProvider:
    def __init__(
        self,
        default_gps_coordinates: tuple[float, float] = (28.6139, 77.2090),
        default_environment_readings: dict[str, float] | None = None,
    ) -> None:
        self.default_gps_coordinates = default_gps_coordinates
        self.default_environment_readings = default_environment_readings or {
            "temperature_c": 24.5,
            "humidity_percent": 58.0,
            "air_quality_index": 42.0,
            "light_lux": 315.0,
        }
        self._actions: dict[str, Callable[..., Any]] = {}
        self._register_builtin_actions()

    def _register_builtin_actions(self) -> None:
        self.register_action("send_sms", self._send_sms)
        self.register_action("get_gps_location", self._get_gps_location)
        self.register_action("capture_image", self._capture_image)
        self.register_action("read_environment", self._read_environment)
        self.register_action("trigger_emergency_alert", self._trigger_emergency_alert)

    def register_action(self, name: str, func: Callable[..., Any]) -> None:
        self._actions[name] = func

    def list_actions(self) -> list[str]:
        return sorted(self._actions)

    def execute(self, name: str, *args: Any, **kwargs: Any) -> Any:
        if name not in self._actions:
            return f"[Gemma4] (function) Called {name} with {args} {kwargs} (plugin not found)"
        return self._actions[name](*args, **kwargs)

    def _send_sms(self, phone_number: str, message: str) -> str:
        return f"[Gemma4] (sms) Sent '{message}' to {phone_number}"

    def _get_gps_location(self) -> str:
        latitude, longitude = self.default_gps_coordinates
        return f"[Gemma4] (gps) Current location: lat={latitude}, lon={longitude}"

    def _capture_image(self, camera_name: str = "default_camera") -> str:
        return f"[Gemma4] (camera) Captured image from {camera_name}"

    def _read_environment(self, sensor_type: str = "all") -> str:
        if sensor_type == "all":
            return f"[Gemma4] (sensor) Readings: {self.default_environment_readings}"
        value = self.default_environment_readings.get(sensor_type)
        if value is None:
            return f"[Gemma4] (sensor) Unknown sensor '{sensor_type}'"
        return f"[Gemma4] (sensor) {sensor_type}={value}"

    def _trigger_emergency_alert(self, message: str) -> str:
        return f"[Gemma4] (alert) Emergency alert triggered: {message}"

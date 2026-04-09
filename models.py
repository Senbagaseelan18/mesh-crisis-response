"""
Pydantic models for Emergency Mesh-Network Router environment.
Defines observations, actions, and state for the mesh network.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
from enum import Enum


class TaskDifficulty(str, Enum):
    """Task difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class DeviceNode(BaseModel):
    """Represents a device node in the mesh network."""
    device_id: str = Field(..., description="Unique identifier for the device")
    position: tuple = Field(..., description="(x, y) coordinates of the device")
    battery_level: float = Field(..., ge=0, le=100, description="Battery percentage (0-100)")
    rssi: float = Field(default=-50, description="Signal strength (RSSI in dBm, typically -30 to -100)")
    is_gateway: bool = Field(default=False, description="Whether this is the gateway device")
    is_active: bool = Field(default=True, description="Whether the device is active")
    hop_count: int = Field(default=0, description="Number of hops from the alert origin")


class MeshObservation(BaseModel):
    """
    Observation of the mesh network state.
    Represents what the agent observes at each step.
    """
    current_device_id: str = Field(..., description="ID of the device currently holding the alert")
    current_rssi: float = Field(..., description="RSSI at current device")
    current_battery: float = Field(..., description="Battery level at current device")
    neighboring_devices: List[DeviceNode] = Field(..., description="List of devices in range")
    gateway_distance: float = Field(..., description="Euclidean distance to gateway")
    hops_taken: int = Field(default=0, description="Number of hops taken so far")
    time_step: int = Field(default=0, description="Current timestep")
    task_difficulty: TaskDifficulty = Field(..., description="Current task difficulty")
    alert_payload: Dict = Field(default_factory=dict, description="Alert metadata")


class MeshAction(BaseModel):
    """
    Action taken by the agent.
    The agent decides which neighboring device to forward the alert to.
    """
    target_device_id: str = Field(..., description="ID of the target device to forward to")
    priority: int = Field(default=1, ge=1, le=5, description="Priority level (1=low, 5=high)")


class MeshState(BaseModel):
    """
    Complete state of the mesh network.
    Represents the full environment state.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    device_map: Dict[str, DeviceNode] = Field(..., description="Map of all devices in network")
    alert_location: str = Field(..., description="Current device holding the alert")
    gateway_location: str = Field(..., description="ID of the gateway device")
    hops_remaining: int = Field(..., description="Maximum remaining hops allowed")
    current_hop: int = Field(default=0, description="Current hop number")
    task_difficulty: TaskDifficulty = Field(..., description="Current task difficulty")
    is_terminal: bool = Field(default=False, description="Whether the episode is terminal")
    success: bool = Field(default=False, description="Whether alert reached gateway")


class RewardInfo(BaseModel):
    """
    Breakdown of reward components for transparency.
    """
    distance_reward: float = Field(default=0.0, description="Reward for moving closer to gateway")
    hop_penalty: float = Field(default=0.0, description="Penalty per hop taken")
    delivery_reward: float = Field(default=0.0, description="Reward for successful delivery")
    battery_penalty: float = Field(default=0.0, description="Penalty for battery depletion")
    total_reward: float = Field(default=0.0, description="Total reward for the step")


class TaskGradeResult(BaseModel):
    """
    Result of programmatic grading for a task.
    """
    difficulty: TaskDifficulty = Field(..., description="Task difficulty")
    score: float = Field(..., ge=0.0, le=1.0, description="Score between 0.0 and 1.0")
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Rate of successful deliveries")
    average_hops: float = Field(default=0.0, description="Average hops to delivery")
    average_reward: float = Field(default=0.0, description="Average reward per episode")
    details: str = Field(default="", description="Additional details about the grade")

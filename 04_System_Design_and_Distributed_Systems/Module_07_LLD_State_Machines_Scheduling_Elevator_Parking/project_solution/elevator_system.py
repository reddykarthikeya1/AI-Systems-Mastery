#!/usr/bin/env python3
"""Module 07: In-Process Architectural Simulation Model: Multi-Car Elevator Dispatch & State Machine Engine.

Implements:
- Finite State Machine (IDLE, MOVING, STOPPED, DOORS_OPEN)
- Directional Dispatching using the LOOK / Elevator Algorithm
- Multi-Car Dispatch Optimization (assigning to most efficient car)
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from enum import StrEnum


class Direction(StrEnum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"


class DoorState(StrEnum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass
class HallCall:
    floor: int
    direction: Direction


class ElevatorCar:
    """Represents a single elevator car running the LOOK scheduling algorithm."""

    def __init__(
        self,
        car_id: int,
        min_floor: int = 1,
        max_floor: int = 20,
        capacity: int = 10,
    ) -> None:
        self.car_id = car_id
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.capacity = capacity

        self.current_floor = min_floor
        self.direction = Direction.IDLE
        self.door_state = DoorState.CLOSED
        self.passenger_count = 0

        # Destination requests made from inside the car or assigned from hall calls
        self.up_stops: set[int] = set()
        self.down_stops: set[int] = set()
        self._lock = threading.Lock()

    def add_destination(self, floor: int) -> None:
        """Adds a stop request to the car."""
        if not (self.min_floor <= floor <= self.max_floor):
            raise ValueError(f"Floor {floor} out of range [{self.min_floor}, {self.max_floor}]")

        with self._lock:
            if floor > self.current_floor:
                self.up_stops.add(floor)
                if self.direction == Direction.IDLE:
                    self.direction = Direction.UP
            elif floor < self.current_floor:
                self.down_stops.add(floor)
                if self.direction == Direction.IDLE:
                    self.direction = Direction.DOWN
            else:
                # Already on this floor: open doors
                self.door_state = DoorState.OPEN

    def step(self) -> int:
        """Simulates one discrete clock tick of elevator physics (LOOK algorithm).

        Returns the floor arrived at, or current floor if idle/stopped.
        """
        with self._lock:
            # If doors were open, close them before moving
            if self.door_state == DoorState.OPEN:
                self.door_state = DoorState.CLOSED

            if self.direction == Direction.UP:
                if self.current_floor < self.max_floor:
                    self.current_floor += 1

                # Check if this floor is a destination stop
                if self.current_floor in self.up_stops:
                    self.up_stops.remove(self.current_floor)
                    self.door_state = DoorState.OPEN

                # Determine if we should continue UP or reverse/idle
                if not any(f > self.current_floor for f in self.up_stops):
                    if self.down_stops:
                        self.direction = Direction.DOWN
                    elif self.up_stops:
                        self.direction = Direction.UP
                    else:
                        self.direction = Direction.IDLE

            elif self.direction == Direction.DOWN:
                if self.current_floor > self.min_floor:
                    self.current_floor -= 1

                # Check if this floor is a destination stop
                if self.current_floor in self.down_stops:
                    self.down_stops.remove(self.current_floor)
                    self.door_state = DoorState.OPEN

                # Determine if we should continue DOWN or reverse/idle
                if not any(f < self.current_floor for f in self.down_stops):
                    if self.up_stops:
                        self.direction = Direction.UP
                    elif self.down_stops:
                        self.direction = Direction.DOWN
                    else:
                        self.direction = Direction.IDLE

            elif self.direction == Direction.IDLE:
                if self.up_stops:
                    self.direction = Direction.UP
                elif self.down_stops:
                    self.direction = Direction.DOWN

            return self.current_floor

    @property
    def has_pending_stops(self) -> bool:
        return bool(self.up_stops or self.down_stops)


class ElevatorController:
    """Manages an elevator bank, dispatching hall calls to the optimal car."""

    def __init__(self, num_cars: int = 3, min_floor: int = 1, max_floor: int = 20) -> None:
        self.cars = [
            ElevatorCar(car_id=i + 1, min_floor=min_floor, max_floor=max_floor)
            for i in range(num_cars)
        ]

    def request_elevator(self, floor: int, direction: Direction) -> ElevatorCar:
        """Dispatches the hall call to the car with lowest cost score."""
        best_car = min(self.cars, key=lambda car: self._calculate_dispatch_cost(car, floor, direction))
        best_car.add_destination(floor)
        return best_car

    def _calculate_dispatch_cost(self, car: ElevatorCar, target_floor: int, requested_direction: Direction) -> int:
        """Calculates distance and directional continuity cost.

        Lower is better.
        - Idle car directly incurs simple distance.
        - Moving car travelling towards the call in the same direction has low penalty.
        - Moving car travelling away or in opposite direction incurs heavy turnaround penalty.
        """
        distance = abs(car.current_floor - target_floor)

        if car.direction == Direction.IDLE:
            return distance

        # Car moving towards request in same direction
        if car.direction == requested_direction:
            if car.direction == Direction.UP and target_floor >= car.current_floor:
                return distance
            if car.direction == Direction.DOWN and target_floor <= car.current_floor:
                return distance

        # Car moving away or in opposite direction -> full cycle turnaround penalty
        return distance + (car.max_floor - car.min_floor) * 2

    def step_all(self) -> dict[int, int]:
        """Steps all cars one tick; returns mapping of car_id -> current_floor."""
        return {car.car_id: car.step() for car in self.cars}

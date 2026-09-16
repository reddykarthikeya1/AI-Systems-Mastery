"""Unit tests for Elevator Dispatch System and LOOK Scheduling Algorithm."""

from __future__ import annotations

import pytest
from elevator_system import (
    Direction,
    DoorState,
    ElevatorCar,
    ElevatorController,
)


def test_single_car_look_algorithm_upward_continuation() -> None:
    car = ElevatorCar(car_id=1, min_floor=1, max_floor=10)
    assert car.current_floor == 1
    assert car.direction == Direction.IDLE

    # Add stops at floor 3 and floor 5
    car.add_destination(3)
    car.add_destination(5)
    assert car.direction == Direction.UP

    # Step 1: moves to floor 2
    f1 = car.step()
    assert f1 == 2
    assert car.door_state == DoorState.CLOSED

    # Step 2: arrives at floor 3 -> opens doors!
    f2 = car.step()
    assert f2 == 3
    assert car.door_state == DoorState.OPEN
    assert 3 not in car.up_stops

    # Step 3: closes doors, moves to floor 4
    f3 = car.step()
    assert f3 == 4
    assert car.door_state == DoorState.CLOSED

    # Step 4: arrives at floor 5 -> opens doors!
    f4 = car.step()
    assert f4 == 5
    assert car.door_state == DoorState.OPEN
    assert not car.has_pending_stops


def test_elevator_reverses_direction_when_topmost_request_served() -> None:
    car = ElevatorCar(car_id=1, min_floor=1, max_floor=10)
    # On floor 1, request floor 4 (UP) and floor 2 (DOWN)
    car.add_destination(4)
    car.down_stops.add(2)  # Simulates someone requesting downward from floor 2

    # Advance until floor 4 is reached
    while car.current_floor < 4:
        car.step()

    assert car.current_floor == 4
    # With no higher UP stops, it should switch direction to DOWN to service floor 2
    car.step()
    assert car.direction == Direction.DOWN


def test_multi_car_controller_assigns_nearest_idle_car() -> None:
    controller = ElevatorController(num_cars=3, min_floor=1, max_floor=20)
    # Position cars at floors 1, 10, 18
    controller.cars[0].current_floor = 1
    controller.cars[1].current_floor = 10
    controller.cars[2].current_floor = 18

    # Hall call at floor 11 going UP should be assigned to Car 2 (current floor 10)
    assigned = controller.request_elevator(floor=11, direction=Direction.UP)
    assert assigned.car_id == 2
    assert 11 in assigned.up_stops


def test_controller_direction_continuity_penalty() -> None:
    controller = ElevatorController(num_cars=2, min_floor=1, max_floor=20)
    car1 = controller.cars[0]
    car2 = controller.cars[1]

    # Car 1 is at floor 8 moving DOWN
    car1.current_floor = 8
    car1.direction = Direction.DOWN

    # Car 2 is at floor 5 and IDLE
    car2.current_floor = 5
    car2.direction = Direction.IDLE

    # Hall call at floor 9 UP:
    # Car 1 is closer (dist 1) but moving away/wrong direction (turnaround penalty).
    # Car 2 is idle at floor 5 (dist 4).
    assigned = controller.request_elevator(floor=9, direction=Direction.UP)
    assert assigned.car_id == 2


def test_out_of_bounds_floor_request_raises() -> None:
    car = ElevatorCar(car_id=1, min_floor=1, max_floor=10)
    with pytest.raises(ValueError, match="out of range"):
        car.add_destination(25)

#!/usr/bin/env python3
"""Module 07 Demo: Live Elevator Bank Simulation with the LOOK Algorithm."""

import sys
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from elevator_system import (
    Direction,
    DoorState,
    ElevatorController,
)


def render_elevator_bank(controller: ElevatorController, max_floor: int = 10) -> None:
    print("\n  Floor | " + " | ".join(f"Car #{c.car_id} ({c.direction.value:<4})" for c in controller.cars))
    print("  " + "-" * 48)
    for fl in range(max_floor, 0, -1):
        row = f"  {fl:4d}  | "
        car_cells = []
        for c in controller.cars:
            if c.current_floor == fl:
                status = "[DOORS OPEN]" if c.door_state == DoorState.OPEN else "[  CAR   ]"
                car_cells.append(f"{status:^15}")
            else:
                stops = ""
                if fl in c.up_stops:
                    stops += "▲"
                if fl in c.down_stops:
                    stops += "▼"
                car_cells.append(f"{stops:^15}")
        row += " | ".join(car_cells)
        print(row)


def main() -> None:
    print("=" * 72)
    print("  MODULE 07: MULTI-CAR ELEVATOR DISPATCH & LOOK SCHEDULING SIMULATION")
    print("=" * 72)

    controller = ElevatorController(num_cars=2, min_floor=1, max_floor=10)
    controller.cars[0].current_floor = 1
    controller.cars[1].current_floor = 8

    print("\n--- Initial Elevator State ---")
    render_elevator_bank(controller, max_floor=10)

    # Dispatch hall calls
    print("\nDispatching Passenger Calls:")
    print("  1. Hall Call: Floor 4 going UP")
    c1 = controller.request_elevator(floor=4, direction=Direction.UP)
    print(f"     -> Assigned to Car #{c1.car_id}")

    print("  2. Hall Call: Floor 7 going DOWN")
    c2 = controller.request_elevator(floor=7, direction=Direction.DOWN)
    print(f"     -> Assigned to Car #{c2.car_id}")

    # Step simulation for 6 ticks
    for tick in range(1, 7):
        print(f"\n--- Simulation Tick #{tick} ---")
        controller.step_all()
        render_elevator_bank(controller, max_floor=10)

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()

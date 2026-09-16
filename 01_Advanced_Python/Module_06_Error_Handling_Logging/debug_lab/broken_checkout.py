#!/usr/bin/env python3
"""Broken Checkout Service demonstrating exception chaining, bare except, and duplicate logger traps."""

import logging
import time

def setup_checkout_logger():
    logger = logging.getLogger("checkout")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def process_card_charge(card_token: str):
    try:
        if not card_token.startswith("tok_"):
            raise ValueError("Invalid merchant token format")
    except:
        print("[WARNING] Caught exception with bare except!")

def submit_order():
    try:
        int("invalid_amount")
    except ValueError as err:
        raise RuntimeError("Payment gateway processing failed")

if __name__ == "__main__":
    for i in range(3):
        log = setup_checkout_logger()
        log.info(f"Transaction step {i+1}")

    process_card_charge("bad_token")

    try:
        submit_order()
    except RuntimeError as e:
        print(f"Caught error: {e}, cause: {e.__cause__} (Expected ValueError cause, got None!)")

"""Tests for Twitter Snowflake Generator."""
from __future__ import annotations

import pytest
from p01_twitter_snowflake_generator import twitter_snowflake_generator


def test_twitter_snowflake_generator():
    id1 = twitter_snowflake_generator(1700000001000, 5, 1)
    id2 = twitter_snowflake_generator(1700000001000, 5, 2)
    assert id2 > id1
    assert id1 > 0

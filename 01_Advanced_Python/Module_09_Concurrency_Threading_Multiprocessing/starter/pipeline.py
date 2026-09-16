"""STARTER - Module 09: Concurrency Threading Multiprocessing

Hybrid Media Processing Pipeline (Threading + Multiprocessing).

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_pipeline.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/pipeline.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
import hashlib
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass

@dataclass
class RawAsset:
    asset_id: str
    url: str
    raw_data: bytes


@dataclass
class ProcessedAsset:
    asset_id: str
    checksum: str
    transformed_size: int
    duration: float


def fetch_media_chunk(asset_id: str) -> RawAsset:
    """Simulates high-speed network download of a raw media file (I/O-Bound)."""
    # [Tier 2] Algorithm: Implement fetch_media_chunk adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_fetch_media_chunk
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 09: implement fetch_media_chunk()")


def transcode_and_hash(asset: RawAsset) -> ProcessedAsset:
    """Simulates CPU-heavy image resizing, frame transformations, and SHA-256 hashing."""
    # [Tier 2] Algorithm: Implement transcode_and_hash adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_transcode_and_hash
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 09: implement transcode_and_hash()")


class HybridMediaPipeline:
    """Orchestrates I/O thread pool downloads followed by multi-process CPU crunching."""

    def __init__(self, io_workers: int = 8, cpu_workers: int | None = None) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_fetch_media_chunk
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 09: implement HybridMediaPipeline.__init__()")


    def run_pipeline(self, asset_ids: list[str]) -> list[ProcessedAsset]:
        # [Tier 2] Algorithm: Coordinate execution pipeline, processing inputs
        #   and aggregating results.
        # HINTS:
        #  - Process items sequentially or in batches, applying transformations.
        #  - Track successes and errors separately for a clean summary.
        # GRADES: test_end_to_end_hybrid_pipeline
        # WARNING: Ensure exceptions from individual items do not crash the
        #   entire batch.
        raise NotImplementedError("Module 09: implement HybridMediaPipeline.run_pipeline()")



def main() -> None:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_fetch_media_chunk
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 09: implement main()")


if __name__ == "__main__":
    main()

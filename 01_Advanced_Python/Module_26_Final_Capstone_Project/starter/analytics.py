"""STARTER - Module 26: Final Capstone Project

High-Performance Polars and DuckDB Analytics Engine for Capstone Platform.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_analytics.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/analytics.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
import duckdb
import polars as pl

class CapstoneAnalytics:

    @staticmethod
    def aggregate_project_budgets(projects_data: list[dict]) -> pl.DataFrame:
        # [Tier 1] Algorithm: Implement
        #   CapstoneAnalytics.aggregate_project_budgets adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_analytics_aggregate_project_budgets
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 26: implement CapstoneAnalytics.aggregate_project_budgets()")


    @staticmethod
    def rank_projects_duckdb(projects_data: list[dict]) -> pl.DataFrame:
        # [Tier 2] Algorithm: Implement CapstoneAnalytics.rank_projects_duckdb
        #   adhering to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_analytics_rank_projects_duckdb
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 26: implement CapstoneAnalytics.rank_projects_duckdb()")

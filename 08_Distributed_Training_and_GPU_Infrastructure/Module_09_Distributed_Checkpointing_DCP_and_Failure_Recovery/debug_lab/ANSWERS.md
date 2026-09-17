# Diagnosis and Fix

## Root Cause
Each rank must save its partitioned tensor shard to a distinct file path containing its process rank: `checkpoint_{tensor_name}_rank_{rank}.pt`.

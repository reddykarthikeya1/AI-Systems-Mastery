# Self-Assessment & Staff Interview Challenges: Memory Hierarchy & Coalescing

## Architectural Interview Scenarios

### Question 1: Uncoalesced Read vs Write Penalty
**Scenario**: In a matrix transpose kernel, you can choose between coalescing the global memory read and leaving the global memory write uncoalesced, or vice versa. Which one causes greater performance degradation?

**Staff-Level Solution**:
Uncoalesced **writes** cause greater performance degradation than uncoalesced **reads**.
- **Reads**: If threads issue strided loads, the L1/L2 cache lines can still provide spatial locality across subsequent warps.
- **Writes**: Global memory writes that are uncoalesced cause multiple partial-cache-line write requests. On architectures with write-back caches, this requires reading the existing cache line into L2, modifying the bytes, and marking it dirty (Read-Modify-Write cycle), saturating the interconnect.
**Rule of Thumb**: Always prioritize coalesced global memory writes! Use shared memory as an intermediate staging buffer to transpose the coordinates so both reads and writes are coalesced.

"""Broken Distributed Checkpoint File Sharding."""
def get_shard_filename(tensor_name: str, rank: int) -> str:
    # BUG: Omits rank identifier, causing simultaneous race condition overwrite
    return f"checkpoint_{tensor_name}.pt"

if __name__ == '__main__':
    names = [get_shard_filename("layers.0.weight", r) for r in range(4)]
    assert len(set(names)) == 1  # Collision!
    print("Filenames:", names)

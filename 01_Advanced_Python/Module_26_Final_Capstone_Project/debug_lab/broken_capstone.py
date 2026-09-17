import sys
from pathlib import Path

mod_dir = Path(__file__).resolve().parent.parent
if str(mod_dir) not in sys.path:
    sys.path.insert(0, str(mod_dir))

from capstone_platform.tasks import CapstoneTaskBroker

def trigger_analytics_export_task(broker: CapstoneTaskBroker):
    # Task worker expects payload key 'target_format' ('json' or 'parquet'),
    # but the API gateway passes 'format'. Task fails with KeyError in worker process!
    task = broker.enqueue("ExportMetrics", {"format": "parquet"})
    return task

def run_worker_loop(broker: CapstoneTaskBroker):
    for task in broker.queue:
        # Worker expects target_format
        fmt = task.payload["target_format"]  # KeyError!
        print(f"Exporting in format: {fmt}")

if __name__ == "__main__":
    broker = CapstoneTaskBroker()
    trigger_analytics_export_task(broker)
    try:
        run_worker_loop(broker)
    except KeyError as err:
        print(f"Cross-subsystem integration failure: KeyError on missing payload key: {err}")

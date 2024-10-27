from datetime import datetime
from typing import List, Optional
import json
from pathlib import Path

class TimeEntry:
    def __init__(self, task_name: str, start_time: datetime):
        self.task_name = task_name
        self.start_time = start_time

    def get_duration(self, next_start_time: Optional[datetime] = None) -> float:
        end = next_start_time or datetime.now()
        return (end - self.start_time).total_seconds()

    def to_dict(self, next_start_time: Optional[datetime] = None) -> dict:
        return {
            "task_name": self.task_name,
            "start_time": self.start_time.isoformat(),
            "duration_seconds": self.get_duration(next_start_time)
        }

class TimeTracker:
    def __init__(self):
        self.current_entry: Optional[TimeEntry] = None
        self.entries: List[TimeEntry] = []
        self.data_dir = Path("time_entries")
        self.data_dir.mkdir(exist_ok=True)

    def start_task(self, task_name: str) -> str:
        if self.current_entry:
            self.entries.append(self.current_entry)
        
        self.current_entry = TimeEntry(task_name, datetime.now())
        return f"Started task: {task_name}"

    def stop_timer(self) -> str:
        if not self.current_entry:
            return "No task is running"
        
        self.entries.append(self.current_entry)
        self._save_session()
        self.current_entry = None
        self.entries = []
        return "Timer stopped"

    def get_current_status(self) -> str:
        if not self.current_entry:
            return "No task is running"
        duration = self.current_entry.get_duration()
        return f"Current task: {self.current_entry.task_name} (running for {duration:.2f} seconds)"

    def _save_session(self) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.data_dir / f"session_{timestamp}.json"
        
        session_data = []
        for i, entry in enumerate(self.entries):
            next_start_time = self.entries[i + 1].start_time if i < len(self.entries) - 1 else datetime.now()
            session_data.append(entry.to_dict(next_start_time))
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)

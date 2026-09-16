import datetime

class TaskTrace:
    def __init__(self, trace_file: str = "trace.log"):
        self.trace_file = trace_file
        
    def log(self, message: str):
        timestamp = datetime.datetime.now().isoformat()
        log_line = f"[{timestamp}] {message}\n"
        print(log_line.strip())
        with open(self.trace_file, "a", encoding="utf-8") as f:
            f.write(log_line)

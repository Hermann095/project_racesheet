from dataclasses import dataclass
from ..enums.enums import LogDetailLevel, LogEventType

@dataclass
class LogEntry():
  text: str
  detailLevel: LogDetailLevel
  type: LogEventType
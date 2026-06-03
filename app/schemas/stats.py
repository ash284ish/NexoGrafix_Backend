from pydantic import BaseModel

class StatsOut(BaseModel):
    total_newsletters: int
    total_new_requests: int
    total_in_progress: int
    total_resolved: int

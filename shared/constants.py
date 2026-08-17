# Shared global application constants
class SystemConstants:
    PROJECT_NAME = "NovaAgent"
    API_V1_PREFIX = "/api/v1"

class TaskStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class MemoryCategories:
    MEETING = "meeting"
    CALENDAR = "calendar"
    NOTE = "note"
    TASK = "task"
    PREFERENCE = "preference"
    DOCUMENT = "document"

class StorageProviders:
    LOCAL = "local"
    SUPABASE = "supabase"

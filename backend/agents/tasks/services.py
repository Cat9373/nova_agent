from sqlalchemy.orm import Session
from backend.database.session import SessionLocal
from backend.services.task import task_service
from backend.schemas.tasks import TaskCreate
from backend.utils.logging import logger
from datetime import datetime, timedelta

class TasksAgentService:
    def process_task_intent(self, prompt: str, user_id: str) -> str:
        """
        Parses task management intents and interacts with TaskService database APIs.
        """
        logger.info(f"TasksAgent processing: '{prompt}'")
        db: Session = SessionLocal()
        try:
            # Parsing heuristics
            if "create" in prompt.lower() or "add" in prompt.lower() or "todo" in prompt.lower():
                content = prompt.replace("create task", "").replace("add task", "").replace("todo", "").strip()
                title = "New Task"
                if ":" in content:
                    parts = content.split(":", 1)
                    title = parts[0].strip()
                    content = parts[1].strip()
                
                # Mock high-priority if requested
                priority = "high" if "urgent" in prompt.lower() or "high" in prompt.lower() else "medium"
                
                task_in = TaskCreate(
                    title=title,
                    description=content or prompt,
                    due_date=datetime.utcnow() + timedelta(days=1), # Default 1 day due date
                    priority=priority
                )
                task = task_service.create_task(db, task_in=task_in, user_id=user_id)
                return f"Task created: '{task.title}' (Priority: {task.priority}) due on {task.due_date.strftime('%Y-%m-%d')}. Indexed in long-term memory."
                
            elif "list" in prompt.lower() or "get" in prompt.lower() or "show" in prompt.lower():
                tasks = task_service.get_user_tasks(db, user_id=user_id)
                if not tasks:
                    return "You do not have any tasks on your todo list."
                summary = "Here are your current tasks:\n"
                for idx, task in enumerate(tasks, 1):
                    summary += f"{idx}. [{task.priority.upper()}] {task.title} - Status: {task.status} (Due: {task.due_date})\n"
                return summary
            else:
                return "I detected a Tasks query. Try typing 'create task: [title]: [description]' or 'list tasks'."
        finally:
            db.close()

tasks_agent_service = TasksAgentService()

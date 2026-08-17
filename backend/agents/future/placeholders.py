from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseAgentInterface(ABC):
    @abstractmethod
    def run_inference(self, prompt: str, user_id: str) -> Dict[str, Any]:
        """
        Runs agent inference workflow using standard state graphs.
        """
        pass


class EmailAgentPlaceholder(BaseAgentInterface):
    """
    [Phase 2 Blueprint]
    Exposes email drafting, reading inbox signals, auto-categorizing, and drafting replies.
    Integrates with Gmail and Outlook OAuth gateways.
    """
    def run_inference(self, prompt: str, user_id: str) -> Dict[str, Any]:
        return {
            "agent": "EmailAgent",
            "status": "placeholder",
            "message": "Inbox reading and auto replies are planned for Phase 2."
        }


class CalendarAgentPlaceholder(BaseAgentInterface):
    """
    [Phase 2 Blueprint]
    Executes double-booking checks, scheduling requests, parsing meeting links,
    and automatic synchronization with Google Calendar / Outlook Calendar APIs.
    """
    def run_inference(self, prompt: str, user_id: str) -> Dict[str, Any]:
        return {
            "agent": "CalendarAgent",
            "status": "placeholder",
            "message": "Calendar event orchestration and auto scheduling are planned for Phase 2."
        }


class MeetingAgentPlaceholder(BaseAgentInterface):
    """
    [Phase 2 Blueprint]
    Processes live audio streams of meetings, outputs transcription text,
    creates summaries, and populates decisions & tasks databases.
    """
    def run_inference(self, prompt: str, user_id: str) -> Dict[str, Any]:
        return {
            "agent": "MeetingAgent",
            "status": "placeholder",
            "message": "Live meeting transcription and summarize pipelines are planned for Phase 2."
        }


class ResearchAgentPlaceholder(BaseAgentInterface):
    """
    [Phase 4 Blueprint]
    Browses internet search providers, parses documents, crawls links,
    and returns comprehensive summaries on domain specific business research.
    """
    def run_inference(self, prompt: str, user_id: str) -> Dict[str, Any]:
        return {
            "agent": "ResearchAgent",
            "status": "placeholder",
            "message": "Deep web browsing and reporting are planned for Phase 4."
        }


class AnalyticsAgentPlaceholder(BaseAgentInterface):
    """
    [Phase 4 Blueprint]
    Executes business query analysis. Evaluates data streams, generates graphs/charts,
    and populates Executive Analytics Dashboard summaries.
    """
    def run_inference(self, prompt: str, user_id: str) -> Dict[str, Any]:
        return {
            "agent": "AnalyticsAgent",
            "status": "placeholder",
            "message": "Enterprise metrics parsing and chart generation are planned for Phase 4."
        }


class SchedulingAgentPlaceholder(BaseAgentInterface):
    """
    [Phase 4 Blueprint]
    Autonomous scheduling assistant mapping conflicts across multiple business calendars
    and organizing meetings without executive supervision.
    """
    def run_inference(self, prompt: str, user_id: str) -> Dict[str, Any]:
        return {
            "agent": "SchedulingAgent",
            "status": "placeholder",
            "message": "Autonomous multi-calendar booking is planned for Phase 4."
        }

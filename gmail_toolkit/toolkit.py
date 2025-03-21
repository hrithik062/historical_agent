from __future__ import annotations

from typing import TYPE_CHECKING, List

from langchain_community.agent_toolkits.base import BaseToolkit
from langchain_core.tools import BaseTool
from pydantic import ConfigDict, Field

from gmail_toolkit.create_draft import GmailCreateDraft
from gmail_toolkit.get_message import GmailGetMessage
from gmail_toolkit.get_thread import GmailGetThread
from gmail_toolkit.search import GmailSearch
from gmail_toolkit.send_message import GmailSendMessage
from gmail_toolkit.utils import build_resource_service

if TYPE_CHECKING:
    # This is for linting and IDE typehints
    from googleapiclient.discovery import Resource  # type: ignore[import]
else:
    try:
        # We do this so pydantic can resolve the types when instantiating
        from googleapiclient.discovery import Resource
    except ImportError:
        pass


SCOPES = ["https://mail.google.com/"]


class GmailToolkit(BaseToolkit):
    """Toolkit for interacting with Gmail.

    *Security Note*: This toolkit contains tools that can read and modify
        the state of a service; e.g., by reading, creating, updating, deleting
        data associated with this service.

        For example, this toolkit can be used to send emails on behalf of the
        associated account.

        See https://python.langchain.com/docs/security for more information.
    """

    api_resource: Resource = Field(default_factory=build_resource_service)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            GmailCreateDraft(api_resource=self.api_resource),
            GmailSendMessage(api_resource=self.api_resource),
            GmailSearch(api_resource=self.api_resource),
            GmailGetMessage(api_resource=self.api_resource),
            GmailGetThread(api_resource=self.api_resource),
        ]

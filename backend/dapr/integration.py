"""
Dapr integration for the Todo application
"""

from dapr.clients import DaprClient
from typing import Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)


class DaprIntegration:
    """
    Class to handle Dapr integration for the Todo application
    """
    
    def __init__(self):
        self.client = DaprClient()
    
    def save_todo_state(self, todo_id: str, todo_data: Dict[str, Any]) -> bool:
        """
        Save todo data to Dapr state store
        """
        try:
            self.client.save_state(
                store_name="statestore",
                key=f"todo-{todo_id}",
                value=json.dumps(todo_data)
            )
            logger.info(f"Saved todo {todo_id} to state store")
            return True
        except Exception as e:
            logger.error(f"Failed to save todo {todo_id} to state store: {e}")
            return False
    
    def get_todo_state(self, todo_id: str) -> Optional[Dict[str, Any]]:
        """
        Get todo data from Dapr state store
        """
        try:
            response = self.client.get_state(
                store_name="statestore",
                key=f"todo-{todo_id}"
            )
            if response.data:
                return json.loads(response.data.decode('utf-8'))
            return None
        except Exception as e:
            logger.error(f"Failed to get todo {todo_id} from state store: {e}")
            return None
    
    def delete_todo_state(self, todo_id: str) -> bool:
        """
        Delete todo data from Dapr state store
        """
        try:
            self.client.delete_state(
                store_name="statestore",
                key=f"todo-{todo_id}"
            )
            logger.info(f"Deleted todo {todo_id} from state store")
            return True
        except Exception as e:
            logger.error(f"Failed to delete todo {todo_id} from state store: {e}")
            return False
    
    def publish_todo_event(self, event_type: str, event_data: Dict[str, Any]) -> bool:
        """
        Publish a todo event to Dapr pub/sub
        """
        try:
            event_payload = {
                "event_type": event_type,
                "data": event_data,
                "timestamp": self._get_timestamp()
            }
            
            self.client.publish_event(
                pubsub_name="pubsub",
                topic_name="todo-events",
                data=json.dumps(event_payload),
                data_content_type="application/json"
            )
            logger.info(f"Published event {event_type} to pub/sub")
            return True
        except Exception as e:
            logger.error(f"Failed to publish event {event_type}: {e}")
            return False
    
    def invoke_backend_service(self, method: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Invoke another service using Dapr service invocation
        """
        try:
            response = self.client.invoke_method(
                app_id="todo-backend",
                method_name=method,
                data=json.dumps(data),
                content_type="application/json"
            )
            return json.loads(response.data.get())
        except Exception as e:
            logger.error(f"Failed to invoke service method {method}: {e}")
            return None
    
    def _get_timestamp(self) -> str:
        """
        Get current timestamp in ISO format
        """
        from datetime import datetime
        return datetime.utcnow().isoformat()
    
    def close(self):
        """
        Close the Dapr client
        """
        self.client.close()
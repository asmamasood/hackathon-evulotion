"""
Kafka producer for todo events using Dapr
"""

import json
from datetime import datetime
from typing import Dict, Any
from dapr.clients import DaprClient
import logging

logger = logging.getLogger(__name__)


class TodoEventProducer:
    """
    Producer for todo-related events using Dapr pub/sub
    """
    
    def __init__(self):
        # Dapr pub/sub is used instead of direct Kafka connection
        # The actual Kafka connection is handled by the Dapr sidecar
        pass
    
    def publish_todo_created(self, todo_data: Dict[str, Any]) -> bool:
        """
        Publish a todo created event via Dapr
        """
        try:
            event_data = {
                "event_type": "todo.created",
                "data": todo_data,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            with DaprClient() as client:
                client.publish_event(
                    pubsub_name="pubsub",
                    topic_name="todo-events",
                    data=json.dumps(event_data),
                    data_content_type="application/json"
                )
            
            logger.info(f"Published todo.created event for todo {todo_data.get('id')}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish todo.created event: {e}")
            return False
    
    def publish_todo_updated(self, todo_id: str, user_id: str, updates: Dict[str, Any]) -> bool:
        """
        Publish a todo updated event via Dapr
        """
        try:
            event_data = {
                "event_type": "todo.updated",
                "data": {
                    "todo_id": todo_id,
                    "user_id": user_id,
                    "updates": updates,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
            with DaprClient() as client:
                client.publish_event(
                    pubsub_name="pubsub",
                    topic_name="todo-events",
                    data=json.dumps(event_data),
                    data_content_type="application/json"
                )
            
            logger.info(f"Published todo.updated event for todo {todo_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish todo.updated event: {e}")
            return False
    
    def publish_todo_deleted(self, todo_id: str, user_id: str) -> bool:
        """
        Publish a todo deleted event via Dapr
        """
        try:
            event_data = {
                "event_type": "todo.deleted",
                "data": {
                    "todo_id": todo_id,
                    "user_id": user_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
            with DaprClient() as client:
                client.publish_event(
                    pubsub_name="pubsub",
                    topic_name="todo-events",
                    data=json.dumps(event_data),
                    data_content_type="application/json"
                )
            
            logger.info(f"Published todo.deleted event for todo {todo_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish todo.deleted event: {e}")
            return False
    
    def publish_todo_completed(self, todo_id: str, user_id: str, completed: bool) -> bool:
        """
        Publish a todo completion status change event via Dapr
        """
        try:
            event_data = {
                "event_type": "todo.completed" if completed else "todo.uncompleted",
                "data": {
                    "todo_id": todo_id,
                    "user_id": user_id,
                    "completed": completed,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
            with DaprClient() as client:
                client.publish_event(
                    pubsub_name="pubsub",
                    topic_name="todo-events",
                    data=json.dumps(event_data),
                    data_content_type="application/json"
                )
            
            logger.info(f"Published todo.completed event for todo {todo_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish todo.completed event: {e}")
            return False
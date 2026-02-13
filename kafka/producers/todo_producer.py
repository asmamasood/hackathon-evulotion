"""
Kafka producer for todo events
"""

from kafka import KafkaProducer
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class TodoEventProducer:
    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',  # Wait for all replicas to acknowledge
            retries=3,
            linger_ms=5,  # Small wait time to batch messages
            batch_size=16384  # Batch size for efficiency
        )

    def publish_todo_created(self, todo_data: Dict[str, Any]):
        """Publish a todo created event"""
        event = {
            "event_type": "todo.created",
            "data": todo_data,
            "timestamp": self._get_timestamp()
        }
        
        try:
            future = self.producer.send('todo-events', event)
            self.producer.flush()  # Wait for send to complete
            logger.info(f"Published todo.created event for todo {todo_data.get('id')}")
        except Exception as e:
            logger.error(f"Failed to publish todo.created event: {e}")
            raise

    def publish_todo_updated(self, todo_data: Dict[str, Any]):
        """Publish a todo updated event"""
        event = {
            "event_type": "todo.updated",
            "data": todo_data,
            "timestamp": self._get_timestamp()
        }
        
        try:
            self.producer.send('todo-events', event)
            self.producer.flush()
            logger.info(f"Published todo.updated event for todo {todo_data.get('id')}")
        except Exception as e:
            logger.error(f"Failed to publish todo.updated event: {e}")
            raise

    def publish_todo_deleted(self, todo_id: str, user_id: str):
        """Publish a todo deleted event"""
        event = {
            "event_type": "todo.deleted",
            "data": {
                "id": todo_id,
                "user_id": user_id
            },
            "timestamp": self._get_timestamp()
        }
        
        try:
            self.producer.send('todo-events', event)
            self.producer.flush()
            logger.info(f"Published todo.deleted event for todo {todo_id}")
        except Exception as e:
            logger.error(f"Failed to publish todo.deleted event: {e}")
            raise

    def publish_todo_completed(self, todo_id: str, user_id: str, completed: bool):
        """Publish a todo completion status change event"""
        event = {
            "event_type": "todo.completed" if completed else "todo.uncompleted",
            "data": {
                "id": todo_id,
                "user_id": user_id,
                "completed": completed
            },
            "timestamp": self._get_timestamp()
        }
        
        try:
            self.producer.send('todo-events', event)
            self.producer.flush()
            logger.info(f"Published todo.completed event for todo {todo_id}")
        except Exception as e:
            logger.error(f"Failed to publish todo.completed event: {e}")
            raise

    def _get_timestamp(self) -> str:
        """Get ISO formatted timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def close(self):
        """Close the producer"""
        self.producer.close()
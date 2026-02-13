"""
Kafka consumer for todo events
"""

from kafka import KafkaConsumer
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class TodoEventConsumer:
    def __init__(self, bootstrap_servers: str = "localhost:9092", group_id: str = "todo-consumer-group"):
        self.consumer = KafkaConsumer(
            'todo-events',
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            heartbeat_interval_ms=3000,
            session_timeout_ms=30000
        )

    def consume_events(self):
        """Consume todo events from Kafka"""
        logger.info("Starting to consume todo events...")
        
        try:
            for message in self.consumer:
                event_data = message.value
                event_type = event_data.get('event_type')
                
                logger.info(f"Received event: {event_type}")
                
                # Process the event based on its type
                if event_type == "todo.created":
                    self._handle_todo_created(event_data)
                elif event_type == "todo.updated":
                    self._handle_todo_updated(event_data)
                elif event_type == "todo.deleted":
                    self._handle_todo_deleted(event_data)
                elif event_type == "todo.completed":
                    self._handle_todo_completed(event_data)
                elif event_type == "todo.uncompleted":
                    self._handle_todo_uncompleted(event_data)
                else:
                    logger.warning(f"Unknown event type: {event_type}")
                    
        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user")
        except Exception as e:
            logger.error(f"Error consuming events: {e}")
        finally:
            self.close()

    def _handle_todo_created(self, event_data: Dict[str, Any]):
        """Handle todo created event"""
        todo_data = event_data.get('data', {})
        logger.info(f"Processing todo created event: {todo_data.get('id')}")
        
        # In a real implementation, you might:
        # - Send notification to user
        # - Update analytics
        # - Trigger other business processes
        print(f"TODO CREATED: {todo_data}")

    def _handle_todo_updated(self, event_data: Dict[str, Any]):
        """Handle todo updated event"""
        todo_data = event_data.get('data', {})
        logger.info(f"Processing todo updated event: {todo_data.get('id')}")
        
        # In a real implementation, you might:
        # - Send notification to user
        # - Update related records
        # - Trigger other business processes
        print(f"TODO UPDATED: {todo_data}")

    def _handle_todo_deleted(self, event_data: Dict[str, Any]):
        """Handle todo deleted event"""
        todo_data = event_data.get('data', {})
        logger.info(f"Processing todo deleted event: {todo_data.get('id')}")
        
        # In a real implementation, you might:
        # - Send notification to user
        # - Clean up related records
        # - Trigger other business processes
        print(f"TODO DELETED: {todo_data}")

    def _handle_todo_completed(self, event_data: Dict[str, Any]):
        """Handle todo completed event"""
        todo_data = event_data.get('data', {})
        logger.info(f"Processing todo completed event: {todo_data.get('id')}")
        
        # In a real implementation, you might:
        # - Send completion notification
        # - Update user statistics
        # - Trigger other business processes
        print(f"TODO COMPLETED: {todo_data}")

    def _handle_todo_uncompleted(self, event_data: Dict[str, Any]):
        """Handle todo uncompleted event"""
        todo_data = event_data.get('data', {})
        logger.info(f"Processing todo uncompleted event: {todo_data.get('id')}")
        
        # In a real implementation, you might:
        # - Send notification to user
        # - Update user statistics
        # - Trigger other business processes
        print(f"TODO UNCOMPLETED: {todo_data}")

    def close(self):
        """Close the consumer"""
        self.consumer.close()
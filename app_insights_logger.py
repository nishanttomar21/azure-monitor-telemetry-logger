import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import time

# OpenTelemetry imports
from opentelemetry import trace, metrics


class AppInsightsLogger:
    def __init__(self, connection_string: Optional[str] = None):
        """Initialize OpenTelemetry with Azure Monitor"""
        self.connection_string = os.environ.get("APPLICATION_INSIGHTS_CONNECTION_STRING") or connection_string

        if not self.connection_string:
            raise ValueError("Application Insights connection string not found")

        self.setup_azure_monitor()
        self.setup_custom_logging()
        self.setup_tracer()
        self.setup_metrics()

    def setup_azure_monitor(self):
        """Manual Azure Monitor setup with INFO level support"""
        from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter
        from opentelemetry._logs import set_logger_provider
        from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
        from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

        # Create log exporter
        log_exporter = AzureMonitorLogExporter(
            connection_string=self.connection_string
        )

        # Set up logger provider
        logger_provider = LoggerProvider()
        set_logger_provider(logger_provider)

        # Add processor
        logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(log_exporter)
        )

        # Create handler with INFO level
        handler = LoggingHandler(
            level=logging.INFO,  # Key: Set to INFO level
            logger_provider=logger_provider
        )

        # Add handler to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)

        print("✅ Manual Azure Monitor setup completed with INFO level")

    def setup_custom_logging(self):
        """Setup Python logging with console output"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_tracer(self):
        """Get the tracer for custom spans"""
        self.tracer = trace.get_tracer(__name__)

    def setup_metrics(self):
        """Setup custom metrics"""
        meter = metrics.get_meter(__name__)
        self.request_counter = meter.create_counter(
            "custom_requests_total",
            description="Total number of custom requests"
        )
        self.processing_time_histogram = meter.create_histogram(
            "processing_time_seconds",
            description="Time spent processing requests"
        )

    def log_info(self, message: str, properties: Optional[Dict[str, Any]] = None):
        """Send info log with optional custom properties"""
        if properties:
            self.logger.info(message, extra=properties)
        else:
            self.logger.info(message)

    def log_warning(self, message: str, properties: Optional[Dict[str, Any]] = None):
        """Send warning log with optional custom properties"""
        if properties:
            self.logger.warning(message, extra=properties)
        else:
            self.logger.warning(message)

    def log_error(self, message: str, properties: Optional[Dict[str, Any]] = None):
        """Send error log with optional custom properties"""
        if properties:
            self.logger.error(message, extra=properties)
        else:
            self.logger.error(message)

    def create_span(self, operation_name: str):
        """Create a custom trace span"""
        return self.tracer.start_as_current_span(operation_name)

    def increment_counter(self, labels: Optional[Dict[str, str]] = None):
        """Increment custom counter metric"""
        self.request_counter.add(1, labels or {})

    def record_processing_time(self, duration_seconds: float, labels: Optional[Dict[str, str]] = None):
        """Record processing time metric"""
        self.processing_time_histogram.record(duration_seconds, labels or {})


# Example usage and testing
def main():
    """Demo the Application Insights logger functionality"""
    try:
        print("Initializing Application Insights...")
        print("Sending startup log...")

        ai_logger = AppInsightsLogger()

        ai_logger.logger.debug("DEBUG: This is a debug message")
        ai_logger.logger.info("INFO: This is an info message")
        ai_logger.logger.warning("WARNING: This is a warning message")
        ai_logger.logger.error("ERROR: This is an error message")
        ai_logger.logger.critical("CRITICAL: This is a critical message")

        ai_logger.log_info("Application started successfully", {
            "version": "1.0.0",
            "environment": "production",
            "startup_time": datetime.now().isoformat()
        })

        time.sleep(2)
        print("✅ Startup log sent, continuing...")

        # Custom trace with span
        with ai_logger.create_span("user_authentication") as span:
            span.set_attribute("user.id", "user123")
            span.set_attribute("auth.method", "oauth2")

            ai_logger.log_info("User authentication process started", {
                "user_id": "user123",
                "auth_method": "oauth2"
            })

            start_time = time.time()
            time.sleep(0.1)  # Simulate work
            end_time = time.time()

            ai_logger.increment_counter({"operation": "authentication"})
            ai_logger.record_processing_time(
                end_time - start_time,
                {"operation": "authentication"}
            )

            span.set_attribute("processing.duration", end_time - start_time)
            ai_logger.log_info("User authentication completed")

        # Data processing example with nested spans
        with ai_logger.create_span("data_processing") as parent_span:
            parent_span.set_attribute("batch.id", "batch_001")
            parent_span.set_attribute("records.count", 500)

            with ai_logger.create_span("data_validation") as child_span:
                child_span.set_attribute("validation.rules", "required_fields")
                ai_logger.log_info("Data validation started", {
                    "batch_id": "batch_001",
                    "validation_type": "required_fields"
                })

            with ai_logger.create_span("data_transformation") as child_span:
                child_span.set_attribute("transformation.type", "normalize")
                ai_logger.log_warning("Data transformation encountered minor issues", {
                    "batch_id": "batch_001",
                    "issues_count": 5
                })

        # Error handling example
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            ai_logger.log_error(f"Division error occurred: {str(e)}", {
                "error_type": "ZeroDivisionError",
                "function": "main",
                "operation": "calculation"
            })

        ai_logger.log_info("Application workflow completed", {
            "total_operations": 3,
            "success_rate": "66.7%"
        })

        print("Logs and traces sent to Application Insights successfully!")
        print("Check Azure Portal > Application Insights > Logs in a few minutes")

    except Exception as e:
        print(f"Error initializing Application Insights logger: {e}")

    finally:
        time.sleep(2)  # Wait for final batch


if __name__ == "__main__":
    main()

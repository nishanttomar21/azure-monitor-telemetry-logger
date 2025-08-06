# Azure Application Insights Logger

This Python application demonstrates how to integrate and send logs, traces, and custom metrics to Azure Application Insights using OpenTelemetry and the Azure Monitor exporter.

## Features

- **Custom logging** with Python's built-in logging module
- **Trace spans** to track distributed operations
- **Custom metrics** for request counts and processing time
- **Manual Azure Monitor setup** with INFO log level support

## Application Insight Logs Screenshot

![App UI Screenshot](/assets/screenshot.png)

## Flow Architecture

```mermaid
flowchart TD
A["Start: Initialize Application Insights Logger"] --> B{"Connection String Provided?"}
B -- No --> Z["Raise Error: Connection String Not Found"]
B -- Yes --> C["Setup Azure Monitor"]
C --> D["Setup Custom Logging"]
D --> E["Setup Tracer"]
E --> F["Setup Metrics"]
F --> G["Logger Ready"]
G --> H["Send Startup Log"]
H --> I["Log Info: Application Started"]
I --> J["User Authentication Span"]
J --> J1["Set Span Attributes"]
J1 --> J2["Log Info: Auth Started"]
J2 --> J3["Simulate Work"]
J3 --> J4["Increment Counter"]
J4 --> J5["Record Processing Time"]
J5 --> J6["Log Info: Auth Completed"]
J6 --> K["Data Processing Span"]
K --> K1["Set Parent Span Attributes"]
K1 --> K2["Data Validation Span"]
K2 --> K3["Set Validation Attributes"]
K3 --> K4["Log Info: Validation Started"]
K4 --> K5["Data Transformation Span"]
K5 --> K6["Set Transformation Attributes"]
K6 --> K7["Log Warning: Transformation Issues"]
K7 --> L["Error Handling"]
L --> L1{"Division by Zero?"}
L1 -- Yes --> L2["Log Error: Division Error"]
L1 -- No --> M["Continue"]
L2 --> M["Continue"]
M --> N["Log Info: Workflow Completed"]
N --> O["End: Logs and Traces Sent"]
```

## Prerequisites

- Python 3.7 or newer
- Azure Application Insights resource with connection string
- Install dependencies with:
    ```bash
    pip install -r requirements.txt
    ```

## Setup

1. Set the environment variable for connection string:
    ```
   export APPLICATION_INSIGHTS_CONNECTION_STRING="<your_connection_string_here>"
   ```

2. Run the application:
    ```
   python app_insights_logger.py
   ```


## Usage

- The logger sends sample logs, including various severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- Sends custom trace spans for user authentication and data processing.
- Records custom metrics for requests and processing duration.
- Errors such as division by zero are logged with details.

## Verify Logs

- Check Azure Portal > Application Insights > Logs.
- Use KQL queries to explore traces, metrics, and custom dimensions.

## Files

- `app_insights_logger.py` - Main application script
- `requirements.txt` - Python dependencies

## Notes

- Logs at INFO level and above are captured.
- Ensure your connection string is valid and has proper permissions.
- The manual logger setup enables better control over log levels.

## License

[MIT License](LICENSE)
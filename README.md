# Temperature Data Pipeline

A Python-based data pipeline for processing, analyzing, and distributing temperature sensor data. This pipeline automates the complete workflow from raw data ingestion to daily reporting and cloud backup, with **Prefect 3.x orchestration** for enhanced reliability and monitoring.

## 🌡️ Overview

This pipeline processes temperature readings collected every 15 minutes from sensor probes, transforms the data into hourly intervals, stores it in a local database, generates visual dashboards, and automatically distributes reports via email while maintaining cloud backups. The pipeline now includes **Prefect orchestration** for improved task management, error handling, and monitoring.

## 🏗️ Architecture

The pipeline consists of five main components orchestrated by Prefect:

```
Raw CSV Data → Data Cleaning → Database Storage → Visualization → Email + S3 Backup
                                    ↓
                        Prefect Orchestration Layer
                     (Scheduling, Monitoring, Retries)
```

## 📁 Project Structure

```
Weekly-Temperature-Data-Pipeline-Python/
├── scripts/
│   ├── data_clean.py          # Data extraction and transformation
│   ├── create_db.py           # Database creation and data loading
│   ├── create_dash.py         # Dashboard generation
│   ├── sendemail.py          # Email automation
│   ├── backup_s3.py          # Cloud backup and cleanup
│   └── complete_pipe.py       # Prefect orchestration layer
├── Weekly_temperature.csv     # Raw temperature data
├── hourly/                    # Cleaned data storage
├── Dashboards/                # Generated visualizations
└── local_db_analytics.db      # SQLite database
```

## 🚀 Features

- **Prefect Orchestration**: Modern workflow management with Prefect 3.x
- **Automated Scheduling**: Built-in cron scheduling every 3 minutes (configurable)
- **Task Retries**: Automatic retry logic with configurable retry counts
- **Comprehensive Logging**: Detailed logging throughout the pipeline
- **Web UI Monitoring**: Real-time pipeline monitoring at http://localhost:4200
- **Automated Data Processing**: Transforms 15-minute interval data to hourly readings
- **Database Integration**: SQLite storage with date-stamped tables
- **Visual Analytics**: Automated dashboard generation with temperature thresholds
- **Email Reports**: Daily automated email delivery with dashboard attachments
- **Cloud Backup**: S3 integration with organized folder structure
- **Error Handling**: Comprehensive exception handling across all modules
- **Data Validation**: File existence checks and data integrity verification

## ⚙️ Setup

### Prerequisites

- Python 3.8+
- Gmail account with App Password enabled
- AWS account with S3 access
- Required Python packages (see Installation)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/gp4store/Weekly-Temperature-Data-Pipeline-Python.git
cd Weekly-Temperature-Data-Pipeline-Python
```

2. Install required packages:
```bash
pip install pandas matplotlib sqlite3 boto3 python-dotenv prefect
```

3. Create a `.env` file in the root directory:
```env
AUTOMATION_EMAIL=your-gmail@gmail.com
AUTOMATION_PASS=your-app-password
EMAIL_SENDER=recipient@email.com
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

### Gmail Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password for the pipeline
3. Use the App Password in your `.env` file (not your regular Gmail password)

### AWS S3 Setup

1. Create an S3 bucket for temperature data storage
2. Update the bucket name in `backup_s3.py`
3. Ensure your AWS credentials have S3 write permissions

### Prefect Setup

1. Start the Prefect server (optional, for UI monitoring):
```bash
prefect server start
```

2. The pipeline will automatically create flows and schedules when run

## 🔄 Pipeline Components

### Orchestration Layer (`scripts/complete_pipe.py`)
- **Prefect 3.x Integration**: Modern workflow orchestration
- **Task Dependencies**: Ensures proper execution order
- **Retry Logic**: Configurable retry attempts (2-3 retries per task)
- **Logging**: Comprehensive logging with Prefect's logger
- **Scheduling**: Built-in cron scheduling support
- **Monitoring**: Real-time pipeline status and metrics

### 1. Data Cleaning (`data_clean.py`)
- Reads raw temperature CSV data
- Samples data every 4 hours (from 15-minute intervals)
- Creates date-stamped cleaned files
- Copies data to backup directory
- **Prefect Integration**: Wrapped as a Prefect task with 2 retries

### 2. Database Creation (`create_db.py`)
- Loads cleaned CSV into SQLite database
- Creates date-stamped tables
- Provides database structure verification
- **Prefect Integration**: Wrapped as a Prefect task with 2 retries

### 3. Dashboard Generation (`create_dash.py`)
- Creates matplotlib visualizations
- Applies temperature threshold lines (25°C - 35°C)
- Saves PNG files with date stamps
- Customizable chart formatting
- **Prefect Integration**: Wrapped as a Prefect task with 2 retries

### 4. Email Automation (`sendemail.py`)
- Sends daily temperature reports
- Attaches dashboard images
- Includes proper MIME formatting
- Comprehensive error handling
- **Prefect Integration**: Wrapped as a Prefect task with 3 retries

### 5. Cloud Backup (`backup_s3.py`)
- Uploads processed data to S3
- Organizes files by year/month/day structure
- Cleans up local files after successful upload
- **Prefect Integration**: Wrapped as a Prefect task with 3 retries

## 🏃‍♂️ Usage

## ⚠️ Important Setup Step
Before running the pipeline, update all file paths in the scripts:
- Replace `/your/path/` with your actual project directory path
- Update S3 bucket name in `backup_s3.py`

### Prefect Orchestrated Execution (Recommended)

#### Option 1: Run with Automatic Scheduling
```bash
python scripts/complete_pipe.py
```
This starts the Prefect server with automatic scheduling (every 3 minutes by default).

#### Option 2: Run Once Manually
Modify `scripts/complete_pipe.py` to uncomment the manual execution section:
```python
if __name__ == "__main__":
    result = temperature_pipeline()
    print("Pipeline execution completed!")
```

#### Option 3: Custom Scheduling
Modify the cron schedule in `scripts/complete_pipe.py`:
```python
temperature_pipeline.serve(
    name="temp-monitoring",
    cron="0 8 * * *",  # Daily at 8 AM
    description="Automated temperature data processing and reporting",
    tags=["temperature", "data-pipeline", "plc"]
)
```

### Manual Execution (Legacy)

Run each component individually:

```bash
# 1. Clean and transform data
python scripts/data_clean.py

# 2. Load data into database
python scripts/create_db.py

# 3. Generate dashboard
python scripts/create_dash.py

# 4. Send email report
python scripts/sendemail.py

# 5. Backup to S3 and cleanup
python scripts/backup_s3.py
```

## 📊 Monitoring and Observability

### Prefect UI Dashboard
Access the Prefect UI at `http://localhost:4200` to monitor:
- **Flow Runs**: Real-time execution status
- **Task Status**: Individual task success/failure
- **Logs**: Detailed execution logs
- **Retry History**: Task retry attempts and outcomes
- **Scheduling**: Upcoming and past scheduled runs

### Log Output
The pipeline provides comprehensive logging:
- Task start/completion messages
- Error details with full stack traces
- Subprocess output from each script
- Success confirmations with output summaries

## 📊 Sample Output

The pipeline generates:
- **Cleaned CSV files**: `Temperature_log_probe1_YYYYMMDD.csv`
- **Database tables**: `Temperature_log_probe1_YYYYMMDD`
- **Dashboard images**: `Daily_temperature_plot_YYYYMMDD.png`
- **S3 backups**: `logs/year=YYYY/month=MM/day=DD/plc-data-YYYYMMDD.csv`
- **Prefect Logs**: Detailed execution logs in Prefect UI

## 🔧 Configuration

### Prefect Scheduling
Modify the schedule in `scripts/complete_pipe.py`:
```python
# Every 3 minutes (default)
cron="*/3 * * * *"

# Daily at 8 AM
cron="0 8 * * *"

# Every hour
cron="0 * * * *"
```

### Task Retries
Adjust retry counts for individual tasks:
```python
@task(name="Clean Temperature Data", retries=2)  # 2 retries
@task(name="Send Email Report", retries=3)       # 3 retries
```

### Temperature Thresholds
Modify the threshold values in `create_dash.py`:
```python
min_temp = 25  # Minimum temperature line
max_temp = 35  # Maximum temperature line
```

### Sampling Interval
Adjust the data sampling in `data_clean.py`:
```python
transformed_log = df.iloc[0:96:4, :]  # Every 4 hours
```

## 🚨 Error Handling

The pipeline includes comprehensive error handling for:
- **Prefect-level**: Task failures, retries, and flow-level error management
- **Script-level**: File not found errors, SMTP authentication failures
- **Database**: Connection issues and query failures
- **Cloud**: S3 upload failures and authentication errors
- **Data**: Format validation and integrity checks

### Error Recovery
- **Automatic Retries**: Tasks automatically retry on failure
- **Detailed Logging**: Full error context in Prefect logs
- **Graceful Degradation**: Pipeline continues where possible
- **Notification**: Email alerts for critical failures

## 📈 Future Enhancements

- **Advanced Scheduling**: Complex scheduling patterns with Prefect
- **Parallel Processing**: Concurrent task execution for independent operations
- **Deployment**: Production deployment with Prefect Cloud or server
- **Containerization**: Docker deployment for better portability
- **Real-time Processing**: Stream processing capabilities
- **Advanced Analytics**: Statistical analysis and anomaly detection
- **Web Interface**: Custom dashboard web application
- **Multiple Sensors**: Support for multiple temperature probes
- **Data Quality Checks**: Automated data validation and cleansing
- **Alerting**: Advanced monitoring and alerting with Prefect

---
# Temperature Data Pipeline

A Python-based data pipeline for processing, analyzing, and distributing temperature sensor data. This pipeline automates the complete workflow from raw data ingestion to daily reporting and cloud backup.

## 🌡️ Overview

This pipeline processes temperature readings collected every 15 minutes from sensor probes, transforms the data into hourly intervals, stores it in a local database, generates visual dashboards, and automatically distributes reports via email while maintaining cloud backups.

## 🏗️ Architecture

The pipeline consists of five main components:

```
Raw CSV Data → Data Cleaning → Database Storage → Visualization → Email + S3 Backup
```

## 📁 Project Structure

```
Weekly-Temperature-Data-Pipeline-Python/
├── scripts/
│   ├── data_clean.py          # Data extraction and transformation
│   ├── create_db.py           # Database creation and data loading
│   ├── create_dash.py         # Dashboard generation
│   ├── sendemail.py          # Email automation
│   └── backup_s3.py          # Cloud backup and cleanup
├── .env                      # Environment variables (not tracked)
├── Weekly_temperature.csv    # Raw temperature data
├── hourly/                   # Cleaned data storage
├── Dashboards/               # Generated visualizations
└── local_db_analytics.db     # SQLite database
```

## 🚀 Features

- **Automated Data Processing**: Transforms 15-minute interval data to hourly readings
- **Database Integration**: SQLite storage with date-stamped tables
- **Visual Analytics**: Automated dashboard generation with temperature thresholds
- **Email Reports**: Daily automated email delivery with dashboard attachments
- **Cloud Backup**: S3 integration with organized folder structure
- **Error Handling**: Comprehensive exception handling across all modules
- **Data Validation**: File existence checks and data integrity verification

## ⚙️ Setup

### Prerequisites

- Python 3.7+
- Gmail account with App Password enabled
- AWS account with S3 access
- Required Python packages (see Installation)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Weekly-Temperature-Data-Pipeline-Python
```

2. Install required packages:
```bash
pip install pandas matplotlib sqlite3 boto3 python-dotenv
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

## 🔄 Pipeline Components

### 1. Data Cleaning (`data_clean.py`)
- Reads raw temperature CSV data
- Samples data every 4 hours (from 15-minute intervals)
- Creates date-stamped cleaned files
- Copies data to backup directory

### 2. Database Creation (`create_db.py`)
- Loads cleaned CSV into SQLite database
- Creates date-stamped tables
- Provides database structure verification

### 3. Dashboard Generation (`create_dash.py`)
- Creates matplotlib visualizations
- Applies temperature threshold lines (25°C - 35°C)
- Saves PNG files with date stamps
- Customizable chart formatting

### 4. Email Automation (`sendemail.py`)
- Sends daily temperature reports
- Attaches dashboard images
- Includes proper MIME formatting
- Comprehensive error handling

### 5. Cloud Backup (`backup_s3.py`)
- Uploads processed data to S3
- Organizes files by year/month/day structure
- Cleans up local files after successful upload

## 🏃‍♂️ Usage

### Manual Execution

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

### Automated Execution

Create a shell script to run the complete pipeline:

```bash
#!/bin/bash
python scripts/data_clean.py && \
python scripts/create_db.py && \
python scripts/create_dash.py && \
python scripts/sendemail.py && \
python scripts/backup_s3.py
```

Schedule with cron for daily execution:
```bash
0 8 * * * /path/to/your/pipeline/run_pipeline.sh
```

## 📊 Sample Output

The pipeline generates:
- **Cleaned CSV files**: `Temperature_log_probe1_YYYYMMDD.csv`
- **Database tables**: `Temperature_log_probe1_YYYYMMDD`
- **Dashboard images**: `Daily_temperature_plot_YYYYMMDD.png`
- **S3 backups**: `logs/year=YYYY/month=MM/day=DD/plc-data-YYYYMMDD.csv`

## 🔧 Configuration

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

### File Paths
Update paths in each script to match your environment setup.

## 🚨 Error Handling

The pipeline includes comprehensive error handling for:
- File not found errors
- SMTP authentication failures
- Database connection issues
- S3 upload failures
- Data format validation

Check console output for detailed error messages and troubleshooting guidance.

## 📈 Future Enhancements

- **Orchestration**: Implement Apache Airflow or similar workflow management
- **Containerization**: Docker deployment for better portability
- **Real-time Processing**: Stream processing capabilities
- **Advanced Analytics**: Statistical analysis and anomaly detection
- **Web Interface**: Dashboard web application
- **Multiple Sensors**: Support for multiple temperature probes
- **Data Quality Checks**: Automated data validation and cleansing
- **Monitoring**: Pipeline health monitoring and alerting

---

**Note**: Remember to keep your `.env` file secure and never commit it to version control. Update the AWS bucket name and file paths according to your specific environment setup.
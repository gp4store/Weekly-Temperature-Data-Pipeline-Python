"""
Prefect 3.x Orchestration Layer for Temperature Pipeline
This imports and orchestrates your existing scripts as separate tasks
"""

import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

from prefect import flow, task, get_run_logger
# Removed SequentialTaskRunner - not needed in Prefect 3.x

# Get the scripts directory
SCRIPTS_DIR = Path(__file__).parent

@task(name="Clean Temperature Data", retries=2)
def run_data_clean():
    """Run the data cleaning script"""
    logger = get_run_logger()
    
    try:
        script_path = SCRIPTS_DIR / "data_clean.py"
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, check=True)
        
        logger.info("Data cleaning completed successfully")
        logger.info(f"Output: {result.stdout}")
        
        return {"status": "success", "output": result.stdout}
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Data cleaning failed: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in data cleaning: {e}")
        raise

@task(name="Create Database", retries=2)
def run_create_db():
    """Run the database creation script"""
    logger = get_run_logger()
    
    try:
        script_path = SCRIPTS_DIR / "create_db.py"
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, check=True)
        
        logger.info("Database creation completed successfully")
        logger.info(f"Output: {result.stdout}")
        
        return {"status": "success", "output": result.stdout}
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Database creation failed: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in database creation: {e}")
        raise

@task(name="Generate Dashboard", retries=2)
def run_create_dash():
    """Run the dashboard creation script"""
    logger = get_run_logger()
    
    try:
        script_path = SCRIPTS_DIR / "create_dash.py"
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, check=True)
        
        logger.info("Dashboard generation completed successfully")
        logger.info(f"Output: {result.stdout}")
        
        return {"status": "success", "output": result.stdout}
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Dashboard generation failed: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in dashboard generation: {e}")
        raise

@task(name="Send Email Report", retries=3)
def run_send_email():
    """Run the email sending script"""
    logger = get_run_logger()
    
    try:
        script_path = SCRIPTS_DIR / "sendemail.py"
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, check=True)
        
        logger.info("Email sent successfully")
        logger.info(f"Output: {result.stdout}")
        
        return {"status": "success", "output": result.stdout}
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Email sending failed: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in email sending: {e}")
        raise

@task(name="Backup to S3", retries=3)
def run_backup_s3():
    """Run the S3 backup script"""
    logger = get_run_logger()
    
    try:
        script_path = SCRIPTS_DIR / "backup_s3.py"
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, check=True)
        
        logger.info("S3 backup completed successfully")
        logger.info(f"Output: {result.stdout}")
        
        return {"status": "success", "output": result.stdout}
        
    except subprocess.CalledProcessError as e:
        logger.error(f"S3 backup failed: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in S3 backup: {e}")
        raise

@flow(
    name="Temperature Data Pipeline",
    description="Daily temperature data processing using existing scripts",
    # Removed problematic flow_run_name with {date} placeholder
    log_prints=True
)
def temperature_pipeline():
    """
    Main pipeline flow that orchestrates existing scripts
    Keeps your original scripts intact while adding orchestration
    """
    logger = get_run_logger()
    logger.info("Starting Temperature Data Pipeline")
    
    # Run each script in sequence
    # Each task waits for the previous one to complete successfully
    
    # Step 1: Clean and transform data
    clean_result = run_data_clean()
    
    # Step 2: Load to database (depends on cleaning)
    db_result = run_create_db()
    
    # Step 3: Generate dashboard (depends on database)
    dashboard_result = run_create_dash()
    
    # Step 4: Send email report (depends on dashboard)
    email_result = run_send_email()
    
    # Step 5: Backup to S3 (can run after cleaning)
    backup_result = run_backup_s3()
    
    logger.info("Temperature Data Pipeline completed successfully!")
    
    return {
        "data_cleaning": clean_result,
        "database": db_result,
        "dashboard": dashboard_result,
        "email": email_result,
        "backup": backup_result
    }

if __name__ == "__main__":
    # Option 1: Run once manually
    # result = temperature_pipeline()
    # print("Pipeline execution completed!")
    
    # Option 2: Serve with schedule (Prefect 3.x)
    print("🚀 Starting Temperature Pipeline Server...")
    print("📅 Schedule: Every 3 minutes")
    print("🌐 View UI at: http://localhost:4200")
    
    temperature_pipeline.serve(
        name="temp-monitoring",
        cron="*/3 * * * *",
        description="Automated temperature data processing and reporting",
        tags=["temperature", "data-pipeline", "plc"]
    )
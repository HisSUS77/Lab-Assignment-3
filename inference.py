#!/usr/bin/env python3
"""
CYBER-DEF25 Challenge - Malware Detection Inference Script
This script loads a trained ML model and analyzes network logs for potential threats.
"""

import os
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import glob
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define paths
MODEL_PATH = '/app/model.pkl'
INPUT_DIR = '/input/logs'
OUTPUT_DIR = '/output'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'alerts.csv')

def load_model(model_path):
    """
    Load the trained malware detection model
    
    Args:
        model_path (str): Path to the pickled model file
        
    Returns:
        model: Loaded ML model
    """
    try:
        logger.info(f"Loading model from {model_path}")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info("Model loaded successfully")
        return model
    except FileNotFoundError:
        logger.error(f"Model file not found at {model_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

def preprocess_logs(log_file):
    """
    Preprocess network log files for analysis
    
    Args:
        log_file (str): Path to the log file
        
    Returns:
        pd.DataFrame: Preprocessed log data
    """
    try:
        logger.info(f"Processing log file: {log_file}")
        
        # Read log file (assuming CSV format)
        # Adjust based on actual log format
        df = pd.read_csv(log_file)
        
        # Add timestamp for tracking
        df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df['source_file'] = os.path.basename(log_file)
        
        logger.info(f"Loaded {len(df)} log entries from {log_file}")
        return df
        
    except Exception as e:
        logger.error(f"Error processing log file {log_file}: {str(e)}")
        raise

def extract_features(df):
    """
    Extract features from log data for model inference
    
    Args:
        df (pd.DataFrame): Raw log data
        
    Returns:
        np.array: Feature matrix
    """
    # This is a placeholder - adjust based on your actual model features
    # Example: assuming the model expects numeric features
    
    # Exclude non-numeric columns
    exclude_cols = ['processed_at', 'source_file', 'timestamp', 'log_message', 
                   'source_ip', 'dest_ip', 'protocol']
    
    feature_columns = [col for col in df.columns 
                      if col not in exclude_cols and df[col].dtype in ['int64', 'float64']]
    
    if not feature_columns or len(feature_columns) == 0:
        logger.warning("No numeric features found, creating dummy features")
        # Create dummy features for demonstration
        return np.random.rand(len(df), 10)
    
    # Select only numeric features
    features = df[feature_columns].select_dtypes(include=[np.number]).values
    
    # Pad or truncate to 10 features (model expects 10)
    n_samples = features.shape[0]
    n_features = features.shape[1]
    
    if n_features < 10:
        logger.info(f"Padding features from {n_features} to 10")
        # Pad with random values
        padding = np.random.rand(n_samples, 10 - n_features)
        features = np.hstack([features, padding])
    elif n_features > 10:
        logger.info(f"Truncating features from {n_features} to 10")
        features = features[:, :10]
    
    logger.info(f"Extracted {features.shape[1]} features from {features.shape[0]} samples")
    
    return features

def detect_threats(model, features, df):
    """
    Use the model to detect potential threats
    
    Args:
        model: Trained ML model
        features (np.array): Feature matrix
        df (pd.DataFrame): Original log data
        
    Returns:
        pd.DataFrame: Detection results with alerts
    """
    try:
        logger.info("Running threat detection...")
        
        # Make predictions
        predictions = model.predict(features)
        
        # Get prediction probabilities if available
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(features)
            threat_probability = probabilities[:, 1] if len(probabilities.shape) > 1 else probabilities
        else:
            threat_probability = predictions
        
        # Create results dataframe
        results = pd.DataFrame({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_file': df['source_file'] if 'source_file' in df.columns else 'unknown',
            'log_entry_id': range(len(predictions)),
            'threat_detected': predictions,
            'threat_probability': threat_probability,
            'severity': ['HIGH' if p > 0.8 else 'MEDIUM' if p > 0.5 else 'LOW' 
                        for p in threat_probability],
            'action_recommended': ['BLOCK' if p > 0.8 else 'MONITOR' if p > 0.5 else 'ALLOW' 
                                  for p in threat_probability]
        })
        
        # Filter only detected threats
        alerts = results[results['threat_detected'] == 1]
        
        logger.info(f"Detected {len(alerts)} potential threats out of {len(results)} log entries")
        
        return alerts
        
    except Exception as e:
        logger.error(f"Error during threat detection: {str(e)}")
        raise

def save_alerts(alerts, output_file):
    """
    Save detection results to output file
    
    Args:
        alerts (pd.DataFrame): Detection results
        output_file (str): Path to output CSV file
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save alerts
        alerts.to_csv(output_file, index=False)
        logger.info(f"Alerts saved to {output_file}")
        
        # Print summary
        if len(alerts) > 0:
            logger.info("\n" + "="*60)
            logger.info("THREAT DETECTION SUMMARY")
            logger.info("="*60)
            logger.info(f"Total Threats Detected: {len(alerts)}")
            logger.info(f"High Severity: {len(alerts[alerts['severity'] == 'HIGH'])}")
            logger.info(f"Medium Severity: {len(alerts[alerts['severity'] == 'MEDIUM'])}")
            logger.info(f"Low Severity: {len(alerts[alerts['severity'] == 'LOW'])}")
            logger.info("="*60 + "\n")
        else:
            logger.info("No threats detected in the analyzed logs")
            
    except Exception as e:
        logger.error(f"Error saving alerts: {str(e)}")
        raise

def main():
    """
    Main execution function
    """
    try:
        logger.info("="*60)
        logger.info("CYBER-DEF25 Malware Detection System - Starting Analysis")
        logger.info("="*60)
        
        # Load the trained model
        model = load_model(MODEL_PATH)
        
        # Find all log files in input directory
        log_files = glob.glob(os.path.join(INPUT_DIR, '*.csv'))
        
        if not log_files:
            logger.warning(f"No log files found in {INPUT_DIR}")
            logger.info("Creating empty alerts file...")
            empty_alerts = pd.DataFrame(columns=[
                'timestamp', 'source_file', 'log_entry_id', 
                'threat_detected', 'threat_probability', 
                'severity', 'action_recommended'
            ])
            save_alerts(empty_alerts, OUTPUT_FILE)
            return
        
        logger.info(f"Found {len(log_files)} log file(s) to process")
        
        # Process all log files
        all_alerts = []
        
        for log_file in log_files:
            try:
                # Preprocess logs
                df = preprocess_logs(log_file)
                
                # Extract features
                features = extract_features(df)
                
                # Detect threats
                alerts = detect_threats(model, features, df)
                
                if len(alerts) > 0:
                    all_alerts.append(alerts)
                    
            except Exception as e:
                logger.error(f"Error processing {log_file}: {str(e)}")
                continue
        
        # Combine all alerts
        if all_alerts:
            final_alerts = pd.concat(all_alerts, ignore_index=True)
        else:
            final_alerts = pd.DataFrame(columns=[
                'timestamp', 'source_file', 'log_entry_id', 
                'threat_detected', 'threat_probability', 
                'severity', 'action_recommended'
            ])
        
        # Save results
        save_alerts(final_alerts, OUTPUT_FILE)
        
        logger.info("Analysis completed successfully")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Fatal error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()

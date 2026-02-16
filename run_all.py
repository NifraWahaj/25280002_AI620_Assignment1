# Nifra Wahaj | 25280002

"""
Automates all steps: Extract → Clean → Analyze 
"""
import subprocess
import sys
from pathlib import Path
import time

def run_command(command, description):
    print("\n" + "="*70)
    print(f"STEP: {description}")
    print("="*70)
    print(f"Running: {command}\n")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=False,
            text=True
        )
        
        elapsed = time.time() - start_time
        print(f"\n✓ SUCCESS - Completed in {elapsed:.1f} seconds")
        return True
        
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        print(f"\n✗ FAILED after {elapsed:.1f} seconds")
        print(f"Error: {e}")
        return False

def main():
    """Run complete pipeline"""
    print("\n" + "="*70)
    print("ELT PIPELINE - COMPLETE RUN")
    print("="*70)
    print("\nThis will run all pipeline steps in sequence:")
    print("  1. Extract data from all sources")
    print("  2. Clean and transform data")
    print("  3. Generate visualizations")
    print("="*70)
    
    response = input("\nProceed? (y/n): ").strip().lower()
    if response != 'y':
        print("Aborted.")
        return
    
    pipeline_start = time.time()
    
    # Step 1: Extract
    success = run_command(
        "python run_pipeline.py",
        "1/4 - Extracting data from NewsAPI, Google Trends, and NASDAQ"
    )
    if not success:
        print("\n⚠ Pipeline stopped due to extraction error")
        print("Check API keys and credentials in .env and ~/.kaggle/")
        sys.exit(1)
    
    # Step 2: Clean
    success = run_command(
        "python -m src.transform_clean",
        "2/4 - Cleaning and transforming data"
    )
    if not success:
        print("\n⚠ Pipeline stopped due to cleaning error")
        sys.exit(1)
    
    # Step 3: Analyze
    success = run_command(
        "python -m src.analyze_visualize",
        "3/4 - Generating visualizations"
    )
    if not success:
        print("\nPipeline stopped due to analysis error")
        sys.exit(1)
    
    # Summary
    total_time = time.time() - pipeline_start
    
    print("\n" + "="*70)
    print("PIPELINE COMPLETED !")
    print("="*70)
    print(f"\n execution time: {total_time/60:.1f} minutes")
    print("\n Generated outputs:")
    print("   Raw data:        data/raw/")
    print("   Cleaned data:    data/cleaned/")
    print("   Quality reports: data/processed/")
    print("   Visualizations:  visualizations/")


if __name__ == "__main__":
    main()

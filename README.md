# NYC 311 Service Dashboard

## Project Overview
A complete data analytics system built for analyzing municipal service disparities across New York City neighborhoods. Processes 2GB+ of 311 service requests on 2024 to identify zip codes with significantly longer response times.

## Quick Start

### Install
git clone https://github.com/bsofc/NYC311-Service-Dashboard
cd NYC311-Service-Dashboard

### Run dashboard
bokeh serve src/dashboard.py --show

### Use CLI tool
python src/borough_complaints.py -h

## What It Does
- **CLI Tool**: Analyze complaint data by date range and borough
- **Dashboard**: Compare service response times across zip codes
- **Processing**: Handles 500,000+ records efficiently

## Key Features
- Interactive Bokeh dashboard with real-time filtering
- Command-line tool for data exploration
- Identifies neighborhoods with 40%+ longer response times
- Deployed on AWS EC2

## Technical Stack
- Python (pandas, Bokeh, argparse)
- AWS EC2, Linux command line
- Git, Jupyter, data visualization

## Project Structure
- `src/dashboard.py` - Interactive dashboard
- `src/borough_complaints.py` - CLI tool
- `data/` - Processed data files
  
## How It Works
1. Load 311 service request data
2. Filter and process records
3. Compute response time averages
4. Display in interactive dashboard
5. Compare neighborhoods

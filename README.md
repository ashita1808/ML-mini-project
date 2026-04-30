
# Airport Ground Optimizer Dashboard

A comprehensive machine learning-powered dashboard for airport ground operations optimization with real-time delay prediction, advanced analytics, and optimization insights.

## Features

### 🚀 Core Functionality
- **ML Delay Prediction**: Advanced machine learning model for flight delay prediction
- **CSV Validation**: Intelligent validation with detailed error reporting and data quality checks
- **Real-time Analytics**: Live dashboard with interactive charts and KPIs

### 📊 Dashboard Components
- **Key Performance Indicators (KPIs)**:
  - Total Flights, Predicted Delays, Delay Rate
  - Average Delay Probability, High-Risk Flights, On-Time Rate

- **Interactive Charts**:
  - Delay Distribution (Doughnut Chart)
  - Hourly Delay Patterns (Line Chart)
  - Airline Performance Comparison (Bar Chart)
  - Top Delay Routes Analysis (Horizontal Bar Chart)

- **Optimization Insights**:
  - High-risk routes identification
  - Peak delay hour analysis
  - Airline performance metrics
  - Smart optimization suggestions

### 🤖 Smart Features
- **CSV Validation**: Comprehensive data validation with warnings and error reporting
- **Prediction Table**: Detailed prediction results with export functionality
- **Smart Suggestions**: AI-powered recommendations for operational improvements
- **API Endpoints**: RESTful APIs for predictions, insights, and KPIs

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd airport-ground-optimizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the dashboard**
   Open your browser and navigate to: `http://127.0.0.1:5000`

## Usage

### Upload Flight Data
1. Prepare your flight data CSV with the required columns:
   - `Month`: Flight month (1-12)
   - `DayOfWeek`: Day of week (1-7)
   - `CRSDepTime`: Scheduled departure time (HHMM format)
   - `CRSArrTime`: Scheduled arrival time (HHMM format)
   - `Distance`: Flight distance in miles
   - `Marketing_Airline_Network`: Airline code (e.g., AA, DL, UA)
   - `Origin`: Origin airport code
   - `Dest`: Destination airport code

2. Click "Choose File" and select your CSV file
3. Click "Analyze & Predict" to process the data

### Sample Data
A sample CSV file (`sample_flights.csv`) is provided for testing the dashboard functionality.

## API Endpoints

- `GET /`: Main dashboard
- `GET /api/predictions`: Get all predictions as JSON
- `GET /api/insights`: Get optimization insights
- `GET /api/kpis`: Get key performance indicators

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Chart.js
- **Machine Learning**: Scikit-learn, Joblib
- **Data Processing**: Pandas, NumPy
- **Visualization**: Chart.js for interactive charts

## Project Structure

```
airport-ground-optimizer/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── sample_flights.csv          # Sample data for testing
├── README.md                   # Project documentation
├── static/
│   └── style.css              # Custom CSS styling
├── templates/
│   └── index.html             # Main dashboard template
├── notebook/
│   └── data/
│       ├── cleaned_flights_data.csv
│       ├── flight_delay_model.pkl
│       ├── EDA_PROJECT.ipynb
│       └── MODEL_TRAINING.ipynb
└── src/
    ├── components/
    │   ├── data_ingestion.py
    │   ├── data_transformation.py
    │   └── model_train.py
    └── pipeline/
        ├── prediction_pipeline.py
        └── training_pipeline.py
```

## Features in Detail

### CSV Validation
- Checks for required columns
- Validates data types and ranges
- Reports missing values and data quality issues
- Provides actionable warnings and error messages

### ML Predictions
- Uses trained Random Forest model for delay prediction
- Provides probability scores for each prediction
- Handles categorical encoding automatically
- Includes fallback mock model for demonstration

### Analytics Dashboard
- **KPIs**: Real-time metrics with visual indicators
- **Charts**: Multiple chart types for comprehensive analysis
- **Insights**: AI-generated optimization recommendations
- **Export**: Download prediction results as CSV

### Smart Suggestions
- Staffing optimization recommendations
- Route management insights
- Departure sequencing suggestions
- Peak hour operational guidance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on the GitHub repository.





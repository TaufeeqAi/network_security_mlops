# Network Security ML Pipeline

This project implements a machine learning pipeline for network security analysis, specifically focusing on phishing detection. It's built with MLOps best practices, including automated data processing, model training, and prediction capabilities.

## Features

- Automated data ingestion and validation
- Data transformation pipeline
- Model training with performance monitoring
- Batch prediction capabilities
- Cloud integration with AWS S3
- Containerized deployment using Docker
- CI/CD pipeline with GitHub Actions

## Project Structure

```
├── Artifacts/                 # Generated artifacts during pipeline execution
├── Network_Data/              # Raw data directory
├── data_schema/              # Data validation schemas
├── final_model/              # Trained model artifacts
├── logs/                     # Application logs
├── network_security/         # Main package directory
│   ├── cloud/                # Cloud integration modules
│   ├── components/           # Pipeline components
│   ├── constants/            # Configuration constants
│   ├── entity/               # Data entities and configurations
│   ├── exception/            # Custom exception handling
│   ├── logging/              # Logging configuration
│   ├── pipeline/             # Training and prediction pipelines
│   └── utils/                # Utility functions
├── notebooks/                # Jupyter notebooks for analysis
├── templates/                # HTML templates for web interface
└── valid_data/              # Validated data directory
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd network_security
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Configure your AWS credentials if using S3
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
```

## Usage

### Training Pipeline

Run the training pipeline:
```bash
python main.py
```

This will:
1. Ingest the data from the source
2. Validate the data against the schema
3. Transform the data for model training
4. Train the model and save artifacts

### Batch Prediction

For batch predictions on new data:
```bash
python batch_prediction.py --input_file path/to/input.csv
```

### Web Interface

Start the web server:
```bash
python app.py
```

Access the web interface at `http://localhost:5000`

## Docker Deployment

Build the Docker image:
```bash
docker build -t network-security .
```

Run the container:
```bash
docker run -p 5000:5000 network-security
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
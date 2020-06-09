# Acquire data public S3 bucket 
python3 src/download_data.py

# Create database
python3 src/model.py

# Generate features
python3 src/generate_features.py

# EDA analysis
python3 src/EDA.py

# Train model
python3 src/train_model.py

# Score model
python3 src/score_model.py

# Evaluate model
python3 src/evaluate_model.py


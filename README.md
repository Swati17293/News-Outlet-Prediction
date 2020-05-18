# News Outlet Prediction


## Are You Following the Right News-Outlet? A Machine Learningbased approach for outlet prediction

This project is an approach to recommend a list ofprobable outlets covering an event of interest. 

To run this project go through the following steps:

### 1. Create the conda environment from the environment.yml file to install the dependencies.
    
    conda env create --name yourenvname --file=environment.yml

### 2. Activate the environment.

    conda activate yourenvname

### 3. Prepare the dataset.
    
    -- apikey = eventregistry API key

    python3 src/data/load_data.py apiKey
    
    python3 src/data/split_data.py

### 4. Pre-process the data

    python3 src/features/preprocess_data.py

### 5. Vectorize the data for future use

    python3 src/features/vectorize_data.py

### 6. Train the model

    python3 src/models/train_model.py

### 7. Generate the predictions

    python3 src/models/predict_model.py

### 8. Evaluate and compare the models

    python3 src/models/evaluate_model.py


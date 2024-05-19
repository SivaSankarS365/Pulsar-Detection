import numpy as np
import json

def preprocess_live_data(live_data):
    # Load preprocessing parameters from file
    with open('preprocessing_parameters.json', 'r') as f:
        preprocessing_parameters = json.load(f)
    feature_means = np.array(preprocessing_parameters['mean'])
    feature_stds = np.array(preprocessing_parameters['std'])
    
    # Normalize features using the loaded parameters
    live_data_normalized = (live_data - feature_means) / feature_stds
    
    # Feature Engineering
    interaction_features = []
    polynomial_features = []
    
    # Interaction Features: products and sums of feature pairs
    for i in range(len(live_data_normalized)):
        for j in range(i + 1, len(live_data_normalized)):
            interaction_features.append(live_data_normalized[i] * live_data_normalized[j])
            interaction_features.append(live_data_normalized[i] + live_data_normalized[j])

    # Polynomial Features: squares and cubes of features
    for feature in live_data_normalized:
        polynomial_features.append(feature ** 2)
        polynomial_features.append(feature ** 3)

    # Statistical Features: mean and variance of existing features
    mean_feature = np.mean(live_data_normalized)
    var_feature = np.var(live_data_normalized)
    
    live_data_normalized = np.concatenate([live_data_normalized, interaction_features, polynomial_features, [mean_feature, var_feature]])
    
    return live_data_normalized

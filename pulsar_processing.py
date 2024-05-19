import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import numpy as np
import json

class SplitRow(beam.DoFn):
    def process(self, element):
        return [element.split(',')]

class FilterMissingValues(beam.DoFn):
    def process(self, element):
        if all(element):
            return [element]
        return []

class ConvertDataTypes(beam.DoFn):
    def process(self, element):
        try:
            # Convert all features to float and the target to int
            features = list(map(float, element[:-1]))
            target = int(element[-1].strip())
            return [features + [target]]
        except ValueError:
            return []


class NormalizeFeatures(beam.DoFn):
    def setup(self):
        self.feature_means = None
        self.feature_stds = None

    def process(self, element):
        features = np.array(element[:-1])
        if self.feature_means is None or self.feature_stds is None:
            self.feature_means = features.mean(axis=0)
            self.feature_stds = features.std(axis=0)
            # Save parameters to file
            with open('preprocessing_parameters.json', 'w') as f:
                json.dump({'mean': self.feature_means.tolist(), 'std': self.feature_stds.tolist()}, f)
        normalized_features = (features - self.feature_means) / self.feature_stds
        return [normalized_features.tolist() + [element[-1]]]

class FeatureEngineering(beam.DoFn):
    def process(self, element):
        features = element[:-1]
        target = element[-1]
        
        # Interaction Features: products and sums of feature pairs
        interaction_features = []
        for i in range(len(features)):
            for j in range(i + 1, len(features)):
                interaction_features.append(features[i] * features[j])
                interaction_features.append(features[i] + features[j])
        
        # Polynomial Features: squares and cubes of features
        polynomial_features = [f ** 2 for f in features] + [f ** 3 for f in features]
        
        # Statistical Features: mean and variance of existing features
        mean_feature = np.mean(features)
        var_feature = np.var(features)
        
        new_features = features + interaction_features + polynomial_features + [mean_feature, var_feature]
        return [new_features + [target]]

def run():
    # Define pipeline options
    pipeline_options = PipelineOptions()

    # Create the pipeline
    with beam.Pipeline(options=pipeline_options) as p:
        lines = (p
                 | 'ReadCSV' >> beam.Create([line.strip() for line in open('modeling/HTRU_2.csv').readlines()[1:]])
                 | 'SplitRows' >> beam.ParDo(SplitRow()))

        cleaned_data = (lines
                        | 'FilterMissingValues' >> beam.ParDo(FilterMissingValues())
                        | 'ConvertDataTypes' >> beam.ParDo(ConvertDataTypes())
                        | 'NormalizeFeatures' >> beam.ParDo(NormalizeFeatures())
                        | 'FeatureEngineering' >> beam.ParDo(FeatureEngineering())
                        | 'FormatResults' >> beam.Map(lambda x: ','.join(map(str, x)))
                        | 'WriteCleanedData' >> beam.io.WriteToText('modeling/HTRU_2_processed', file_name_suffix='.csv'))

if __name__ == '__main__':
    run()
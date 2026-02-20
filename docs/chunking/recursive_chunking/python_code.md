def create_python_document():
    """
    Creates a sample Python document for testing code chunking.
    """
    python_code = """
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data(filepath):
    \"\"\"
    Load data from CSV file
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        Pandas DataFrame containing the data
    \"\"\"
    df = pd.read_csv(filepath)
    print(f"Loaded data with {df.shape[0]} rows and {df.shape[1]} columns")
    return df

def preprocess_data(df, target_column):
    \"\"\"
    Preprocess the data for training
    
    Args:
        df: Input DataFrame
        target_column: Name of the target column
        
    Returns:
        X, y for model training
    \"\"\"
    # Handle missing values
    df = df.fillna(df.mean())
    
    # Split features and target
    X = df.drop(target_column, axis=1)
    y = df[target_column]
    
    return X, y

class ModelTrainer:
    \"\"\"
    Class to handle model training and evaluation
    \"\"\"
    def __init__(self, model_type='rf', random_state=42):
        \"\"\"Initialize the trainer\"\"\"
        self.random_state = random_state
        if model_type == 'rf':
            self.model = RandomForestClassifier(random_state=random_state)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    def train(self, X, y, test_size=0.2):
        \"\"\"Train the model with train-test split\"\"\"
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state
        )
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_preds = self.model.predict(X_train)
        test_preds = self.model.predict(X_test)
        
        train_acc = accuracy_score(y_train, train_preds)
        test_acc = accuracy_score(y_test, test_preds)
        
        print(f"Training accuracy: {train_acc:.4f}")
        print(f"Testing accuracy: {test_acc:.4f}")
        
        return {
            'model': self.model,
            'X_test': X_test,
            'y_test': y_test,
            'test_acc': test_acc
        }
    
    def get_feature_importance(self, feature_names):
        \"\"\"Get feature importance from the model\"\"\"
        if not hasattr(self.model, 'feature_importances_'):
            raise ValueError("Model doesn't have feature importances")
        
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        result = []
        for i in indices:
            result.append({
                'feature': feature_names[i],
                'importance': importances[i]
            })
        
        return result

if __name__ == "__main__":
    # Example usage
    filepath = "data/dataset.csv"
    df = load_data(filepath)
    
    X, y = preprocess_data(df, target_column="target")
    
    trainer = ModelTrainer(model_type='rf')
    results = trainer.train(X, y, test_size=0.25)
    
    # Print feature importance
    importances = trainer.get_feature_importance(X.columns)
    print("\\nFeature Importance:")
    for item in importances[:5]:
        print(f"- {item['feature']}: {item['importance']:.4f}")
"""
    return python_code

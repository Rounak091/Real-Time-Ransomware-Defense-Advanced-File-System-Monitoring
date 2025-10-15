import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from models.feature_engineering import create_dataset

class ModelTrainer:
    def __init__(self):
        self.models = {
            'random_forest': None,
            'svm': None
        }
        self.metrics = {
            'random_forest': {
                'accuracy': 0.0,
                'auc_score': 0.0,
                'classification_report': {
                    '0': {},
                    '1': {},
                    'macro avg': {},
                    'weighted avg': {}
                }
            },
            'svm': {
                'accuracy': 0.0,
                'auc_score': 0.0,
                'best_params': {
                    'C': None,
                    'gamma': None,
                    'kernel': None
                },
                'best_cv_score': 0.0
            }
        }
    
    def load_data(self):
        """Load processed dataset"""
        try:
            df = pd.read_csv("data/processed/dataset.csv")
            X = df.drop(['label', 'timestamp', 'file_path', 'file_name', 'file_extension', 'event_type'], axis=1, errors='ignore')
            y = df['label']

            # Handle missing values
            X = X.fillna(0)

            # Apply feature scaling
            try:
                preprocessor = joblib.load("data/models/preprocessor.joblib")
                scaler = preprocessor['scaler']
                X = scaler.transform(X)
                print("Applied feature scaling")
            except Exception as e:
                print(f"Warning: Could not load scaler, using unscaled features: {e}")

            print(f"Loaded data: {X.shape[0]} samples, {X.shape[1]} features")
            print(f"Class distribution: {y.value_counts().to_dict()}")

            return X, y

        except Exception as e:
            print(f"Error loading data: {e}")
            # Create dataset if it doesn't exist
            return create_dataset()
    
    def train_random_forest(self, X, y):
        """Train Random Forest classifier"""
        print("=== Training Random Forest Classifier ===")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        rf_model = RandomForestClassifier(
            n_estimators=1000,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        )
        
        rf_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = rf_model.predict(X_test)
        y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = rf_model.score(X_test, y_test)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        print(f"Random Forest Accuracy: {accuracy:.4f}")
        print(f"Random Forest AUC: {auc_score:.4f}")
        print(classification_report(y_test, y_pred))
        
        self.models['random_forest'] = rf_model
        self.metrics['random_forest'] = {
            'accuracy': accuracy,
            'auc_score': auc_score,
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        return rf_model, X_test, y_test
    
    def train_svm(self, X, y):
        """Train SVM classifier with hyperparameter tuning"""
        print("=== Training SVM Classifier ===")
        # Split data

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Hyperparameter tuning with GridSearchCV
        param_grid = {
            'C': [0.1, 1, 10, 100],
            'gamma': [1, 0.1, 0.01, 0.001],
            'kernel': ['rbf', 'linear', 'poly', 'sigmoid']
        }

        grid = GridSearchCV(
            SVC(probability=True, random_state=42, class_weight='balanced'),
            param_grid,
            refit=True,
            verbose=1,
            cv=3,
            scoring='accuracy'
        )

        grid.fit(X_train, y_train)

        print(f"Best SVM parameters: {grid.best_params_}")
        print(f"Best CV score: {grid.best_score_:.4f}")

        svm_model = grid.best_estimator_

        y_pred = svm_model.predict(X_test)
        y_pred_proba = svm_model.predict_proba(X_test)[:, 1]

        accuracy = svm_model.score(X_test, y_test)
        auc_score = roc_auc_score(y_test, y_pred_proba)

        print(f"SVM Accuracy: {accuracy:.4f}")
        print(f"SVM AUC: {auc_score:.4f}")
        print(classification_report(y_test, y_pred))

        self.models['svm'] = svm_model
        self.metrics['svm'] = {
            'accuracy': accuracy,
            'auc_score': auc_score,
            'best_params': grid.best_params_,
            'best_cv_score': grid.best_score_
        }

        return svm_model
    
    def cross_validate(self, model, X, y, model_name="model"):
        """Perform cross-validation"""
        print(f"=== Cross-validating {model_name} ===")
        
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
        print(f"Cross-validation scores: {cv_scores}")
        print(f"Mean CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        return cv_scores
    
    def plot_feature_importance(self, model, feature_names, top_n=10):
        """Plot feature importance"""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            plt.figure(figsize=(10, 6))
            plt.title("Feature Importances")
            plt.bar(range(top_n), importances[indices[:top_n]])
            plt.xticks(range(top_n), [feature_names[i] for i in indices[:top_n]], rotation=45)
            plt.tight_layout()
            plt.savefig('data/models/feature_importance.png')
            plt.show()
            print("Feature importance plot saved to data/models/feature_importance.png")
        else:
            print("Model does not have feature_importances_ attribute")
    
    def save_model(self, model, filename):
        """Save trained model"""
        joblib.dump(model, filename)
        print(f"Model saved to {filename}")
    
    def save_metrics(self, filename="data/models/model_metrics.json"):
        """Save model metrics"""
        import json
        
        # Convert numpy types to Python types for JSON serialization
        def convert_types(obj):
            if isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(item) for item in obj]
            else:
                return obj
        
        metrics_serializable = convert_types(self.metrics)
        
        with open(filename, 'w') as f:
            json.dump(metrics_serializable, f, indent=2)
        
        print(f"Metrics saved to {filename}")
    
    def train_all_models(self):
        """Complete training pipeline"""
        print("=== Starting Model Training Pipeline ===")
        
        # Load data
        X, y = self.load_data()
        
        if X.shape[0] == 0:
            print("No data available for training!")
            return
        
        # Train models
        rf_model, X_test, y_test = self.train_random_forest(X, y)
        svm_model = self.train_svm(X, y)
        
        # Cross-validation
        self.cross_validate(rf_model, X, y, "Random Forest")
        self.cross_validate(svm_model, X, y, "SVM")
        
        # Plot feature importance
        try:
            preprocessor = joblib.load("data/models/preprocessor.joblib")
            feature_names = preprocessor['feature_columns']
        except:
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        self.plot_feature_importance(rf_model, feature_names)
        
        # Save models
        self.save_model(rf_model, "data/models/rf_model.joblib")
        self.save_model(svm_model, "data/models/svm_model.joblib")
        # Save metrics
        self.save_metrics(
            "data/models/model_metrics.json"
        )
        
        print("=== Model Training Complete ===")
        print("Saved models:")
        print("- data/models/rf_model.joblib")
        print("- data/models/svm_model.joblib")
        print("- data/models/model_metrics.json")
        

# Main execution
if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train_all_models()
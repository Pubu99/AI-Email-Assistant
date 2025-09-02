"""
Comprehensive model evaluation script for the Email Assistant
"""
import torch
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    T5Tokenizer, 
    T5ForConditionalGeneration
)
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, 
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
import json
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    def __init__(self, test_data_path: str = "../data/processed/test_data.json"):
        """Initialize the evaluator with test data"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.test_data = self._load_test_data(test_data_path)
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        
    def _load_test_data(self, path: str) -> pd.DataFrame:
        """Load and preprocess test data"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    
    def evaluate_intent_classifier(self, model_dir: str) -> Dict:
        """Evaluate the intent classification model"""
        logger.info("Evaluating intent classifier...")
        
        # Load model and tokenizer
        tokenizer = DistilBertTokenizerFast.from_pretrained(model_dir)
        model = DistilBertForSequenceClassification.from_pretrained(model_dir).to(self.device)
        model.eval()
        
        # Make predictions
        predictions = []
        true_labels = []
        
        with torch.no_grad():
            for text, label in zip(self.test_data['text'], self.test_data['intent']):
                inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(self.device)
                outputs = model(**inputs)
                pred = torch.argmax(outputs.logits, dim=1).item()
                predictions.append(pred)
                true_labels.append(label)
        
        # Calculate metrics
        accuracy = accuracy_score(true_labels, predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(
            true_labels, predictions, average='weighted'
        )
        
        # Generate classification report
        report = classification_report(true_labels, predictions, output_dict=True)
        
        # Create confusion matrix
        cm = confusion_matrix(true_labels, predictions)
        self._plot_confusion_matrix(cm, list(set(true_labels)), "intent_confusion_matrix.png")
        
        metrics = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "classification_report": report
        }
        
        self._print_intent_metrics(metrics)
        return metrics
    
    def evaluate_reply_generator(self, model_dir: str) -> Dict:
        """Evaluate the reply generation model"""
        logger.info("Evaluating reply generator...")
        
        # Load model and tokenizer
        tokenizer = T5Tokenizer.from_pretrained(model_dir)
        model = T5ForConditionalGeneration.from_pretrained(model_dir).to(self.device)
        model.eval()
        
        # Generation metrics
        bleu_scores = []
        rouge1_scores = []
        rouge2_scores = []
        rougeL_scores = []
        
        # Sample outputs for qualitative analysis
        sample_outputs = []
        
        with torch.no_grad():
            for text, reference in zip(self.test_data['text'][:100], self.test_data['reply'][:100]):
                # Generate reply
                input_text = f"generate reply: {text}"
                inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True).to(self.device)
                outputs = model.generate(**inputs, max_length=150, num_return_sequences=1)
                generated_reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                # Calculate BLEU score
                bleu = sentence_bleu([reference.split()], generated_reply.split())
                bleu_scores.append(bleu)
                
                # Calculate ROUGE scores
                rouge_scores = self.rouge_scorer.score(reference, generated_reply)
                rouge1_scores.append(rouge_scores['rouge1'].fmeasure)
                rouge2_scores.append(rouge_scores['rouge2'].fmeasure)
                rougeL_scores.append(rouge_scores['rougeL'].fmeasure)
                
                # Save sample outputs
                if len(sample_outputs) < 5:
                    sample_outputs.append({
                        "input": text,
                        "reference": reference,
                        "generated": generated_reply,
                        "metrics": {
                            "bleu": bleu,
                            "rouge1": rouge_scores['rouge1'].fmeasure,
                            "rouge2": rouge_scores['rouge2'].fmeasure,
                            "rougeL": rouge_scores['rougeL'].fmeasure
                        }
                    })
        
        metrics = {
            "bleu_score": np.mean(bleu_scores),
            "rouge1_score": np.mean(rouge1_scores),
            "rouge2_score": np.mean(rouge2_scores),
            "rougeL_score": np.mean(rougeL_scores),
            "sample_outputs": sample_outputs
        }
        
        self._print_generation_metrics(metrics)
        return metrics
    
    def _plot_confusion_matrix(self, cm: np.ndarray, labels: List[str], filename: str):
        """Plot and save confusion matrix"""
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.savefig(filename)
        plt.close()
    
    def _print_intent_metrics(self, metrics: Dict):
        """Print intent classification metrics in a readable format"""
        print("\n=== Intent Classification Metrics ===")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1 Score: {metrics['f1']:.4f}")
        print("\nDetailed Classification Report:")
        print(pd.DataFrame(metrics['classification_report']).transpose())
    
    def _print_generation_metrics(self, metrics: Dict):
        """Print generation metrics in a readable format"""
        print("\n=== Reply Generation Metrics ===")
        print(f"Average BLEU Score: {metrics['bleu_score']:.4f}")
        print(f"Average ROUGE-1 F1: {metrics['rouge1_score']:.4f}")
        print(f"Average ROUGE-2 F1: {metrics['rouge2_score']:.4f}")
        print(f"Average ROUGE-L F1: {metrics['rougeL_score']:.4f}")
        
        print("\nSample Generations:")
        for i, sample in enumerate(metrics['sample_outputs'], 1):
            print(f"\nExample {i}:")
            print(f"Input: {sample['input']}")
            print(f"Reference: {sample['reference']}")
            print(f"Generated: {sample['generated']}")
            print(f"Metrics: BLEU={sample['metrics']['bleu']:.4f}, ROUGE-L={sample['metrics']['rougeL']:.4f}")

def main():
    """Run the evaluation pipeline"""
    evaluator = ModelEvaluator()
    
    # Evaluate intent classifier
    intent_metrics = evaluator.evaluate_intent_classifier("models/intent_classifier")
    
    # Evaluate reply generator
    generation_metrics = evaluator.evaluate_reply_generator("models/reply_generator")
    
    # Save metrics to file
    all_metrics = {
        "intent_classifier": intent_metrics,
        "reply_generator": generation_metrics
    }
    
    with open("evaluation_results.json", "w") as f:
        json.dump(all_metrics, f, indent=2)
    
    logger.info("Evaluation completed. Results saved to evaluation_results.json")

if __name__ == "__main__":
    main()

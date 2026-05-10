from transformers import pipeline
import torch

# Используем стандартный пайплайн, он самый надежный
def analyze_emotions(text):
    try:

        classifier = pipeline("sentiment-analysis")
        results = classifier(text)


        label = results[0]['label'].lower()
        score = results[0]['score']

     
        if label == 'positive':
            return [{'label': 'joy', 'score': score}]
        else:
            return [{'label': 'sadness', 'score': score}]

    except Exception as e:
        print(f"Error: {e}")
        return [{"label": "error", "score": 0.0}]
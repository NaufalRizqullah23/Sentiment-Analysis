import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = 'mdhugol/indonesia-bert-sentiment-classification'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

dataset = pd.read_csv('datasethalf.csv', encoding='iso-8859-1')

content_list = [str(content) for content in dataset['Tweet']]
max_length = max(len(sequence) for sequence in content_list)

tokenized_content = tokenizer(
    content_list, padding=True, truncation=True, max_length=max_length, return_tensors='pt')

outputs = model(tokenized_content.input_ids, tokenized_content.attention_mask)
predicted_labels = torch.argmax(outputs.logits, dim=1)

dataset['label'] = predicted_labels.tolist()

dataset.to_csv('labeled_dataset.csv', index=False)

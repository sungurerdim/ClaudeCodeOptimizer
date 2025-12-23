# Project: ML Model Serving Pipeline

Build a machine learning model serving pipeline for text classification.

## Requirements

### Core Features
1. **Model Management**
   - Load models from disk (sklearn, pytorch)
   - Model versioning (v1, v2, etc.)
   - Hot-swap models without restart
   - Model metadata (accuracy, training date, features)

2. **Inference API**
   - POST /predict - Single prediction
   - POST /batch-predict - Batch predictions (max 100)
   - Request format: { "text": "...", "model_version": "v1" }
   - Response: { "label": "...", "confidence": 0.95, "latency_ms": 12 }

3. **Preprocessing Pipeline**
   - Text cleaning (lowercase, remove special chars)
   - Tokenization
   - Feature extraction (TF-IDF, embeddings)
   - Pipeline configuration per model

4. **Performance**
   - Request queuing for high load
   - Batching for GPU efficiency
   - Caching for repeated inputs
   - Timeout handling

5. **Monitoring**
   - Request latency histogram
   - Prediction distribution
   - Model performance drift detection
   - Error rate tracking

6. **CLI Tools**
   - `mlserve load <model_path>` - Load new model
   - `mlserve list` - List loaded models
   - `mlserve stats` - Show statistics
   - `mlserve benchmark <model> <n>` - Run benchmark

### Technical Requirements
- FastAPI for serving
- scikit-learn for basic models
- Optional PyTorch support
- Redis for caching (optional, fallback to in-memory)
- Prometheus metrics
- Async request handling
- Tests with pytest

### Project Structure
```
mlserve/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── models/
│   │   ├── registry.py    # Model registry
│   │   ├── loader.py      # Model loading
│   │   └── base.py        # Base model interface
│   ├── preprocessing/
│   │   ├── pipeline.py
│   │   ├── text.py
│   │   └── features.py
│   ├── inference/
│   │   ├── engine.py      # Inference engine
│   │   └── batching.py    # Request batching
│   ├── monitoring/
│   │   ├── metrics.py
│   │   └── drift.py
│   └── cli/
│       └── commands.py
├── tests/
├── models/               # Sample models
└── pyproject.toml
```

### API Examples
```python
# Single prediction
POST /predict
{
  "text": "This product is amazing!",
  "model_version": "sentiment-v2"
}
# Response
{
  "label": "positive",
  "confidence": 0.92,
  "latency_ms": 15,
  "model_version": "sentiment-v2"
}

# Batch prediction
POST /batch-predict
{
  "texts": ["Great!", "Terrible.", "Okay I guess"],
  "model_version": "sentiment-v2"
}
# Response
{
  "predictions": [
    {"label": "positive", "confidence": 0.98},
    {"label": "negative", "confidence": 0.95},
    {"label": "neutral", "confidence": 0.67}
  ],
  "total_latency_ms": 45,
  "model_version": "sentiment-v2"
}
```

### Configuration
```yaml
# config.yaml
models_dir: ./models
default_model: sentiment-v2
max_batch_size: 32
batch_timeout_ms: 50
cache:
  enabled: true
  ttl_seconds: 3600
  max_size: 10000
monitoring:
  enabled: true
  port: 9090
```

## Success Criteria
- Models load and predict correctly
- Batch predictions work efficiently
- Caching improves repeated request latency
- Metrics exposed and accurate
- Hot model swap works without downtime
- CLI tools functional

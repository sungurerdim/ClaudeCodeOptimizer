# ML/AI Rules
*Specific parameters and patterns*

## LLM Best Practices [CRITICAL]

### API Usage
| Pattern | Implementation |
|---------|----------------|
| Retry | Exponential backoff for 429/5xx |
| Streaming | Use for responses > 100 tokens |
| Caching | Cache identical prompts |
| Cost Tracking | Log tokens per request |

### Structured Output
- Use JSON mode or structured outputs (not string parsing)
- Use function/tool calling for actions
- Validate output against schema

### RAG Configuration

| Parameter | Typical Value |
|-----------|---------------|
| Chunk Size | 512-1024 tokens |
| Chunk Overlap | 10-20% |
| Top-K Retrieval | 3-10 documents |

**Always**: Rerank results, include source attribution

---

## Training Essentials

- **Reproducibility**: Set all random seeds (numpy, torch, random)
- **Checkpoints**: Save every N epochs/steps
- **Metrics**: Log loss, accuracy, learning rate

---

## Framework Gotchas

### PyTorch
- `model.eval()` + `torch.no_grad()` for inference
- Save `state_dict()`, not full model
- `device_map="auto"` for large models

### TensorFlow
- `@tf.function` for graph mode performance
- `tf.data` pipeline for efficient loading

### HuggingFace
- Fast tokenizers when available
- `device_map="auto"` for multi-GPU

---

## Inference Optimization

| Technique | Benefit |
|-----------|---------|
| Batching | Higher throughput |
| Quantization (INT8) | 2-4x speedup, minor quality loss |
| KV Cache | Faster autoregressive generation |

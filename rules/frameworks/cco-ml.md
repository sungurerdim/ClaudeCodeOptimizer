# ML/AI Specialized
*Machine learning and AI development rules*

## Training (ML:Training)
**Trigger:** {ml_training_deps}

- **Seed-All**: Set reproducible random seeds for reproducibility
- **Checkpoint-Save**: Save model checkpoints regularly during training
- **Metrics-Log**: Log training metrics (loss, accuracy, etc.)
- **GPU-Utilize**: Optimize GPU memory utilization with batch sizing

## LLM Orchestration (ML:LLM)
**Trigger:** {llm_orchestration_deps}

### Prompt Engineering
- **Prompt-Template**: Versioned prompt templates with clear structure
- **Explicit-Instructions**: Specific instructions, not vague guidance
- **Positive-Framing**: State what to do, not what to avoid
- **Context-Motivation**: Explain WHY instructions matter for better generalization

### API Best Practices
- **Token-Limit**: Respect context limits, use context awareness when available
- **Retry-Backoff**: Retry with exponential backoff for rate limits and transient errors
- **Cost-Track**: Track API costs per operation and user
- **Prompt-Cache**: Cache identical prompts for cost savings (use cached_content when available)
- **Streaming**: Use streaming for long responses to improve perceived latency

### Structured Output
- **Structured-Output**: Use structured outputs/JSON mode for reliable parsing
- **Function-Calling**: Use tool/function calling for actions, not string parsing
- **Schema-Validation**: Validate LLM output against expected schema

### RAG Patterns
- **RAG-Chunk**: Chunk documents appropriately (512-1024 tokens typical)
- **Embedding-Model**: Use appropriate embedding model for domain
- **Reranking**: Use reranking for improved retrieval quality
- **Source-Attribution**: Include source references in generated responses

## Inference (ML:Inference)
**Trigger:** {inference_deps}

- **Batch-Infer**: Batch for throughput
- **Quantize-Prod**: Quantization for production
- **Timeout-Guard**: Inference timeout limits
- **Memory-Manage**: Clear model memory

## ML SDK (ML:SDK)
**Trigger:** {ai_sdk_deps}

- **Key-Rotate**: API key rotation
- **Rate-Limit**: Handle rate limits gracefully
- **Response-Validate**: Validate API responses
- **Fallback-Model**: Fallback to alternative models

## LangChain (ML:LangChain)
**Trigger:** {langchain_deps}

- **Chain-Compose**: Compose chains with LCEL
- **Memory-Manage**: Configure appropriate memory type
- **Callbacks-Use**: Use callbacks for observability
- **Vector-Store**: Choose appropriate vector store
- **Agent-Tools**: Define clear tool descriptions

## LlamaIndex (ML:LlamaIndex)
**Trigger:** {llamaindex_deps}

- **Index-Choose**: Choose index type (VectorStore, List, Tree)
- **Node-Parser**: Configure appropriate node parser
- **Retriever-Tune**: Tune retriever parameters (top_k, similarity)
- **Response-Synthesizer**: Choose response synthesis strategy
- **Storage-Persist**: Persist indices for reuse

## HuggingFace (ML:HuggingFace)
**Trigger:** {huggingface_deps}

- **Pipeline-Use**: Use pipelines for common tasks
- **Tokenizer-Fast**: Use fast tokenizers when available
- **Device-Map**: Use device_map="auto" for large models

## PyTorch (ML:PyTorch)
**Trigger:** {pytorch_deps}

- **Device-Agnostic**: Write device-agnostic code
- **Grad-Context**: Use no_grad for inference
- **DataLoader-Workers**: Configure num_workers for loading
- **Model-Save**: Save state_dict, not full model
- **Mixed-Precision**: Use torch.amp for mixed precision

## TensorFlow (ML:TensorFlow)
**Trigger:** {tensorflow_deps}

- **Graph-Mode**: Use @tf.function decorator for performance
- **Dataset-Pipeline**: Use tf.data for efficient input pipelines
- **Mixed-Precision**: Use mixed precision for training performance

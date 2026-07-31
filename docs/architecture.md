# Architecture Notes

The orchestration layer is deliberately provider-isolated: `src.ai_summary` takes structured profiling information and emits plain text. This keeps the reporting flow available without credentials and leaves a narrow seam for OpenAI, LiteLLM, Ollama, a LangGraph workflow, or an MCP-exposed tool implementation.

For production deployments, place large uploads in object storage, execute `run_pipeline` in a queue worker, persist job metadata, and authenticate the FastAPI boundary.

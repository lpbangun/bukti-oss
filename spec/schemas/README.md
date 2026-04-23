# JSON Schemas

Machine-readable JSON Schema definitions for every object in the protocol.

Each schema file pairs with a document in `../docs/` that explains the shape in prose. The JSON Schema is the normative definition; the prose is explanatory.

Forthcoming in v0.1-draft:
- `voi.schema.json`
- `entity.schema.json`
- `ai-agent-entity.schema.json`
- `capability.schema.json`
- `confidence-score.schema.json`
- `has-capability-edge.schema.json`
- `agent-capability-edge.schema.json`
- `provenance.schema.json`
- `capability-provenance.schema.json`
- `agent-card.schema.json`
- `skills-md-frontmatter.schema.json`
- MCP tool input/output schemas (one per tool).

All schemas will declare `"$schema": "https://json-schema.org/draft/2020-12/schema"`.

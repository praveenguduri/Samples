Business Glossary Management

Goal: Capture authoritative glossary terms with governance context.

Tasks:

Define DB schema for glossary term (term_name, definition, calc_rules, owner, review_cycle).
Add export/import capability for glossary
Build UI/API for CRUD glossary terms.
Create glossary registry dashboard (search, filter by domain).
Enable relationships between terms (synonym_of, parent_of).
Add governance workflow fields (status: draft, approved, retired).
Implement change-log and review history tracking.
Connect glossary ownership to identity system

Enrichment & Cataloging

Goal: Enrich assets with profiling, pattern recognition, and glossary mappings.

Tasks:

Fetch basic profiling information (row count, distinct count, null %, min/max).
Store profiling results in asset_doc under "profiling".
Build lexical matcher: compare column names against glossary terms.
Add semantic similarity check (NLP embedding search).
Generate candidate glossary mappings with confidence score.
Create steward validation workflow (approve/reject mapping).
Enrich asset_doc with validated business terms + quality signals.
Build catalog search across enriched metadata (by term, by system, by owner).

Semantic Construction

Goal: Build semantic entities and relationships in the graph.

Tasks:

Build prompt interface for entity creation (“Eg: Create Customer entity”).
Parse entity prompt → intent (entity scope, attributes, relationships).
Query enriched catalog for candidate attributes.
Draft entity_def with attributes + suggested mappings.
Enable collaborative refinement (add/remove attributes, pick sources).
Store entity_def + semantic mappings in Firestore.
Implement mapping types (direct, derived, composite, temporal).
Push validated entities/mappings into Neo4j/Graphiti.
Build graph explorer UI (nodes = entities, edges = relationships).

example:

prompt: "Create Customer entity with segment and CLV score"
entity_def = {cust_id, name, email, segment, clv_score}
mappings = {cust_id -> crm.customer_id, clv_score -> model.output}
push_to_graph(entity_def, mappings)

Materialization

Goal: Turn semantic entities into operational data products.
Translate entity_def → SQL across sources (join, filter, transform).


Phase 1: OneTru Repository → Manual Onboarding → Asset Catalog → Business Glossary
         ↓
Phase 2: Asset Catalog + Business Glossary → AI Enrichment → Enhanced Catalog
         ↓
Phase 3: Enhanced Catalog + User Prompts → Entity Builder → Knowledge Graph
         ↓
Phase 4: Knowledge Graph + Requirements → SQL Generation → Materialized Entities → NL Queries

# Reference architecture

These diagrams are explanatory discussion-draft artifacts. They communicate the logical relationships the specification expects; they do not mandate a product architecture.

## AI forensic-readiness evidence path

```mermaid
flowchart TB
    subgraph S[Evidence sources]
        ID[Identity and authority]
        AI[Agent and model events]
        CTX[Context memory and retrieval]
        ACT[Tools cloud SaaS and data]
    end
    COL[Protected collection and correlation]
    NORM[Evidence normalization]
    GRAPH[Timeline and AIRG reconstruction]
    RESP[Containment recovery and validation]
    ID --> COL
    AI --> COL
    CTX --> COL
    ACT --> COL
    COL --> NORM
    NORM --> GRAPH
    GRAPH --> RESP
```

## Consequential action chain

```mermaid
flowchart LR
    H[Human principal] -->|instructs| A[Agent A]
    A -->|retrieves| M[Memory or RAG]
    M -->|influences| A
    A -->|delegates| B[Agent B]
    B -->|assumes| I[Delegated identity]
    I -->|invokes| T[Tool or API]
    T -->|modifies| S[Persistent state]
```

## Dependency-aware containment

```mermaid
flowchart TB
    START[Compromised trajectory] --> INV[Inventory authority and dependencies]
    INV --> FUT[Terminate future access]
    INV --> STATE[Find persistent and derived state]
    INV --> CHILD[Find child tasks and downstream consumers]
    FUT --> FIX[Reverse or compensate]
    STATE --> FIX
    CHILD --> FIX
    FIX --> TEST[Validate containment independently]
    TEST --> CLOSE[Record residual risk and close]
```

The canonical diagram source used for static validation is stored in [`canonical-diagrams.json`](canonical-diagrams.json).


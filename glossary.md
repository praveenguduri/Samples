semantics/                          (database name)
├─ Credit/                          (collection = Global Domain)
├─ Marketing/                       (collection = Global Domain)
├─ Fraud/                          (collection = Global Domain)
│
├─ ws_credit_analysis_2025/  (collection = Workspace Domain)
├─ ws_fraud_analysis_2025/  (collection = Workspace Domain)
├─ ws_marketing_q4_2024/     (collection = Workspace Domain)  
│
└─ workspaces/                      (collection = Workspace Registry)
   ├─ credit_analysis/         (document)
   │  ├─ name: "Credit Analysis"
   │  ├─ status: "active"
   │  ├─ domains: ["Credit", "Fraud"]
   │  └─ collections: {             // Map of domain to collection name
   │     "Credit": "ws_credit_analysis_2025",
   │     "Fraud": "ws_fraud_analysis_2025"
   │  }
   │
   └─ marketing_analysis/            (document)
      ├─ name: "Marketing Workspace"
      ├─ status: "active"
      ├─ domains: ["Marketing", "Credit"]
      └─ collections: {
        "Marketing": "ws_marketing_q4_2024",
        "Credit": "ws_credit_analysis_2025"
      }



Global Collections

Format: {DomainName}
Examples: Credit, Marketing, Fraud

Workspace Collections

Single domain: ws_{workspaceId}
Multi-domain with domain-specific: ws_{workspaceId}_{DomainName}

# Kubernetes Application Architecture - Simplified

```mermaid
graph TB
    subgraph "External"
        INTERNET[Internet Users]
        ELB[AWS Load Balancer<br/>ac899d32ff32446b99943283a14bdf2c-483269548.us-west-2.elb.amazonaws.com]
    end

    subgraph "Kubernetes Cluster"
        subgraph "Services"
            SVC_FRONT[frontend Service<br/>LoadBalancer<br/>172.20.223.54:80]
            SVC_CATALOG[prodcatalog Service<br/>ClusterIP<br/>172.20.245.160:5000]
            SVC_DETAIL[proddetail Service<br/>ClusterIP<br/>172.20.92.48:3000]
        end

        subgraph "Application Pods"
            FRONT[frontend Pod<br/>10.10.66.38]
            CATALOG[prodcatalog Pod<br/>10.10.72.166]
            DETAIL[proddetail Pod<br/>10.10.113.70]
        end
    end

    %% External traffic flow
    INTERNET --> ELB
    ELB --> SVC_FRONT
    SVC_FRONT --> FRONT

    %% Internal service communication
    FRONT -->|HTTP calls| SVC_CATALOG
    FRONT -->|HTTP calls| SVC_DETAIL
    SVC_CATALOG --> CATALOG
    SVC_DETAIL --> DETAIL

    classDef pod fill:#90EE90,stroke:#006400,stroke-width:2px
    classDef service fill:#87CEEB,stroke:#4682B4,stroke-width:2px
    classDef external fill:#DDA0DD,stroke:#8B008B,stroke-width:2px

    class FRONT,CATALOG,DETAIL pod
    class SVC_FRONT,SVC_CATALOG,SVC_DETAIL service
    class INTERNET,ELB external
```

## Application Flow
1. **Internet Users** → **AWS Load Balancer** → **Frontend Service** → **Frontend Pod**
2. **Frontend Pod** → **Product Catalog Service** → **Product Catalog Pod**
3. **Frontend Pod** → **Product Detail Service** → **Product Detail Pod**

*Note: No persistent databases found in the cluster - applications appear to be stateless.*

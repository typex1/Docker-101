# Kubernetes Cluster Architecture Diagram

## Overview
This diagram shows the current state of the Kubernetes cluster including nodes, namespaces, pods, services, and their connectivity.

```mermaid
graph TB
    subgraph "EKS Cluster"
        subgraph "Node: ip-10-10-71-224"
            N1[Node: ip-10-10-71-224<br/>10.10.71.224]
            subgraph "kube-system pods (N1)"
                AWS1[aws-node-5gx8q<br/>CNI Plugin]
                CORE1[coredns-5b8cc885bc-6dxfv<br/>10.10.78.36]
                PROXY1[kube-proxy-8cf9s]
            end
            subgraph "workshop pods (N1)"
                FRONT[frontend-5576879b89-5wbtx<br/>10.10.66.38]
                CATALOG[prodcatalog-7dbb95d7c-j66hx<br/>10.10.72.166]
            end
        end

        subgraph "Node: ip-10-10-114-177"
            N2[Node: ip-10-10-114-177<br/>10.10.114.177]
            subgraph "kube-system pods (N2)"
                AWS2[aws-node-f6ngm<br/>CNI Plugin]
                PROXY2[kube-proxy-pbjpb]
            end
            subgraph "workshop pods (N2)"
                DETAIL[proddetail-6c5d9cfc78-h98lz<br/>10.10.113.70]
            end
            subgraph "amazon-guardduty pods (N2)"
                GUARD2[aws-guardduty-agent-8wd9q<br/>CrashLoopBackOff]
            end
        end

        subgraph "Node: ip-10-10-145-53"
            N3[Node: ip-10-10-145-53<br/>10.10.145.53]
            subgraph "kube-system pods (N3)"
                AWS3[aws-node-z5gb2<br/>CNI Plugin]
                CORE2[coredns-5b8cc885bc-s46pr<br/>10.10.156.162]
                PROXY3[kube-proxy-krh8w]
                METRICS1[metrics-server-84fb868dff-24qql<br/>10.10.140.215]
                METRICS2[metrics-server-84fb868dff-55t64<br/>10.10.141.114]
            end
            subgraph "amazon-guardduty pods (N3)"
                GUARD1[aws-guardduty-agent-nzgbs<br/>CrashLoopBackOff]
                GUARD3[aws-guardduty-agent-ssb5q<br/>CrashLoopBackOff]
            end
        end
    end

    subgraph "Services"
        SVC_FRONT[frontend Service<br/>LoadBalancer<br/>172.20.223.54]
        SVC_CATALOG[prodcatalog Service<br/>ClusterIP<br/>172.20.245.160:5000]
        SVC_DETAIL[proddetail Service<br/>ClusterIP<br/>172.20.92.48:3000]
        SVC_DNS[kube-dns Service<br/>ClusterIP<br/>172.20.0.10:53]
        SVC_METRICS[metrics-server Service<br/>ClusterIP<br/>172.20.24.86:443]
    end

    subgraph "External"
        ELB[AWS Load Balancer<br/>ac899d32ff32446b99943283a14bdf2c-483269548.us-west-2.elb.amazonaws.com]
        INTERNET[Internet]
    end

    %% Service to Pod connections
    SVC_FRONT --> FRONT
    SVC_CATALOG --> CATALOG
    SVC_DETAIL --> DETAIL
    SVC_DNS --> CORE1
    SVC_DNS --> CORE2
    SVC_METRICS --> METRICS1
    SVC_METRICS --> METRICS2

    %% Application connectivity
    FRONT -.->|HTTP calls| SVC_CATALOG
    FRONT -.->|HTTP calls| SVC_DETAIL
    CATALOG -.->|may call| SVC_DETAIL

    %% External connectivity
    INTERNET --> ELB
    ELB --> SVC_FRONT

    %% DNS resolution
    FRONT -.->|DNS queries| SVC_DNS
    CATALOG -.->|DNS queries| SVC_DNS
    DETAIL -.->|DNS queries| SVC_DNS

    %% Node networking
    AWS1 -.->|Pod networking| N1
    AWS2 -.->|Pod networking| N2
    AWS3 -.->|Pod networking| N3

    %% Proxy connections
    PROXY1 -.->|Service proxy| N1
    PROXY2 -.->|Service proxy| N2
    PROXY3 -.->|Service proxy| N3

    classDef runningPod fill:#90EE90,stroke:#006400,stroke-width:2px
    classDef crashingPod fill:#FFB6C1,stroke:#DC143C,stroke-width:2px
    classDef service fill:#87CEEB,stroke:#4682B4,stroke-width:2px
    classDef node fill:#F0E68C,stroke:#DAA520,stroke-width:2px
    classDef external fill:#DDA0DD,stroke:#8B008B,stroke-width:2px

    class FRONT,CATALOG,DETAIL,AWS1,AWS2,AWS3,CORE1,CORE2,PROXY1,PROXY2,PROXY3,METRICS1,METRICS2 runningPod
    class GUARD1,GUARD2,GUARD3 crashingPod
    class SVC_FRONT,SVC_CATALOG,SVC_DETAIL,SVC_DNS,SVC_METRICS service
    class N1,N2,N3 node
    class ELB,INTERNET external
```

## Key Components

### Namespaces
- **kube-system**: Core Kubernetes components (DNS, metrics, networking)
- **workshop**: Application workloads (frontend, product catalog, product detail)
- **amazon-guardduty**: Security monitoring (currently experiencing issues)

### Application Architecture
- **Frontend**: Web interface exposed via LoadBalancer service
- **Product Catalog**: Internal service providing catalog data
- **Product Detail**: Internal service providing detailed product information

### Network Flow
1. External traffic enters through AWS Load Balancer
2. Load Balancer routes to frontend service
3. Frontend communicates with backend services (prodcatalog, proddetail)
4. All pods use CoreDNS for service discovery
5. CNI plugin (aws-node) handles pod networking
6. kube-proxy manages service routing on each node

### Current Issues
- GuardDuty agents are in CrashLoopBackOff state across all nodes
- This may indicate configuration or permission issues with the GuardDuty setup

Generated on: Wednesday, 2025-10-29T12:37:35.376+00:00

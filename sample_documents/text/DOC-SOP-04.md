# Production Deployment, Change Advisory Board (CAB) & Rollback SOP
Doc Code: DOC-SOP-04 | Type: SOP | Version: 1.0
Department: ENG_DEV | Organization: ApexNova Global Technologies

## Section 4.1: Standard & Emergency CAB Approval
All production software deployments require a submitted Change Request (CR) approved by the Change Advisory Board (CAB) at least 24 hours prior to release window. Emergency hotfixes require dual sign-off from VP Engineering and Director of SecOps.

## Section 4.2: Automated Canary Deployment Strategy
Deployments must proceed via canary rollout: 5% traffic for 30 minutes, 25% for 1 hour, and 100% only if error budget degradation remains below 0.05%.

## Section 4.3: Automated Rollback Criteria
If p99 latency spikes by >25% or 5xx server error rate exceeds 0.1%, automated deployment orchestrators trigger an immediate rollback to the previous stable release artifact.

## Section 4.4: Deployment Blackout Windows
No standard production deployments are permitted on Fridays after 14:00 UTC or during major global peak retail holidays without explicit CTO exemption.


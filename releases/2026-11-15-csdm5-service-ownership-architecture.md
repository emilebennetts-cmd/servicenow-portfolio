# CSDM 5 service ownership architecture — CMDB case study extension

**Release:** 15 November 2026, Sydney.  
**Public page:** [CMDB / IRE Assurance — CSDM 5](../cmdb-ire-assurance.html#csdm-ownership).  
**Classification:** SOURCE-ONLY reviewed model; PROPOSED native model. Zero new DEV-VERIFIED or PRODUCTION-VERIFIED claims.

## 1. The client's pain & history
A large enterprise CMDB may collect infrastructure data without a reliable bridge between business applications, deployed service instances, service ownership and offerings. This is a representative scenario, not a customer-specific measured outcome.

## 2. The ServiceNow solution
Expanded the existing CMDB/IRE technical deep dive with a responsive four-part CSDM model (business application, service instance, business service, service offering), three keyboard-accessible disclosure scenarios and six concrete native acceptance gates. The page explicitly rejects the misconception that conceptual adjacency proves a direct CMDB relationship. It includes the current Australia-family label Technology Management Service for `cmdb_ci_service_technical`.

## 3. Architectural best practices, evidence and verification
Reviewed the restricted Diagnostic Workbench guided runbook and CMDB issue-pattern governance; reference model only, no private source published. Design prioritises OOTB CMDB Health, IRE, CI Class Manager, CSDM and Service Portfolio Management. Relationships must be evidence-backed, ownership human-attested and status NOT ASSESSED where source coverage is missing. Regression contract `scripts/test_csdm_ownership_architecture.py` validates identifiers, source labels, mobile layout, no embedded images/scripts or private links, and explicit verification boundaries. GitHub Actions outcome requires independent post-push read-back.

Official public guidance (ServiceNow Australia release; updated 12 March 2026): [CSDM domains](https://www.servicenow.com/docs/r/servicenow-platform/common-service-data-model-csdm/csdm-conceptual-model.html), [Service Portfolio Management](https://www.servicenow.com/docs/r/it-service-management/service-portfolio-management/SPM2-services.html), [CMDB Health](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/overview-cmdb-health.html).

**Licensing:** Static website none; native deployments require target-specific verification of Service Portfolio Management, CMDB/IRE/Health, ITOM Discovery/Service Mapping, Service Graph, IntegrationHub, App Engine/custom tables, ATF, roles and third-party rights. No entitlement sign-off performed.

**Publication safeguards:** No secret, customer record, restricted GitHub source, original screenshot, private Drive link or image published. Original screenshot approval remains **0 / HOLD**. Target DEV execution, current plugin/ACL verification, production acceptance and image-by-image publication approval remain outstanding.

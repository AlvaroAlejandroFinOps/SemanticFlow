# ==============================================================================
# Terraform Semantic Modeling as Code (SMaC) Example
# Microsoft Fabric + Databricks Unity Catalog Deployment
# ==============================================================================

terraform {
  required_providers {
    semanticflow = {
      source  = "AlvaroAlejandroFinOps/semanticflow"
      version = "~> 1.0.0"
    }
  }
}

provider "semanticflow" {
  fabric_token     = var.azure_fabric_bearer_token
  databricks_host  = var.databricks_workspace_url
  databricks_token = var.databricks_personal_access_token
}

# 1. Inspección y verificación de Quality Gate en tiempo de plan
data "semanticflow_schema" "core_sales" {
  schema_file = "${path.module}/schemas/esquema_relacional.md"
  min_score   = 75.0
}

output "verified_cqs_score" {
  value       = data.semanticflow_schema.core_sales.cqs_score
  description = "Puntuación de calidad semántica cQS verificada."
}

# 2. Despliegue automatizado del modelo TMDL en Microsoft Fabric
resource "semanticflow_fabric_semantic_model" "sales_mart" {
  workspace_id = var.fabric_workspace_guid
  model_name   = "Enterprise_Sales_TMDL"
  schema_file  = data.semanticflow_schema.core_sales.schema_file
  min_score    = 75.0
  mode         = "DirectLake"
}

# 3. Sincronización de gobernanza y PII en Databricks Unity Catalog
resource "semanticflow_unity_catalog_model" "sales_governance" {
  catalog_name = "corp_lakehouse"
  schema_name  = "gold_sales"
  schema_file  = data.semanticflow_schema.core_sales.schema_file
  min_score    = 75.0
  tag_pii      = true
}

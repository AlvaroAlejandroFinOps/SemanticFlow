use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum EntityRole {
    Dimension,
    Fact,
    Bridge,
    Outrigger,
    Calculated,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum DataType {
    String,
    Int64,
    Double,
    Decimal,
    Boolean,
    Datetime,
    Date,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Attribute {
    pub id: String,
    pub name: String,
    pub data_type: DataType,
    pub is_key: bool,
    pub is_hidden: bool,
    pub description: Option<String>,
    pub is_pii: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Measure {
    pub id: String,
    pub name: String,
    pub expression: String,
    pub description: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Entity {
    pub id: String,
    pub name: String,
    pub role: EntityRole,
    pub description: Option<String>,
    pub attributes: Vec<Attribute>,
    pub metrics: Vec<Measure>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Relationship {
    pub id: String,
    pub name: String,
    pub from_entity_id: String,
    pub from_attribute_id: String,
    pub to_entity_id: String,
    pub to_attribute_id: String,
    pub cardinality: String,
    pub is_active: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CanonicalProject {
    pub project_name: String,
    pub entities: Vec<Entity>,
    pub relationships: Vec<Relationship>,
}

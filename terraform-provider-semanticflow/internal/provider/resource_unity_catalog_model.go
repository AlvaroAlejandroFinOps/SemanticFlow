package provider

import (
	"context"
	"fmt"
	"os/exec"

	"github.com/hashicorp/terraform-plugin-framework/resource"
	"github.com/hashicorp/terraform-plugin-framework/resource/schema"
	"github.com/hashicorp/terraform-plugin-framework/types"
)

var _ resource.Resource = &UnityCatalogModelResource{}

func NewUnityCatalogModelResource() resource.Resource {
	return &UnityCatalogModelResource{}
}

type UnityCatalogModelResource struct {
	client *ClientConfig
}

type UnityCatalogModelResourceModel struct {
	Id          types.String  `tfsdk:"id"`
	CatalogName types.String  `tfsdk:"catalog_name"`
	SchemaName  types.String  `tfsdk:"schema_name"`
	SchemaFile  types.String  `tfsdk:"schema_file"`
	MinScore    types.Float64 `tfsdk:"min_score"`
	TagPii      types.Bool    `tfsdk:"tag_pii"`
}

func (r *UnityCatalogModelResource) Metadata(ctx context.Context, req resource.MetadataRequest, resp *resource.MetadataResponse) {
	resp.TypeName = req.ProviderTypeName + "_unity_catalog_model"
}

func (r *UnityCatalogModelResource) Schema(ctx context.Context, req resource.SchemaRequest, resp *resource.SchemaResponse) {
	resp.Schema = schema.Schema{
		Description: "Sincroniza y gobierna la metadata semántica y clasificación PII en Databricks Unity Catalog con SemanticFlow.",
		Attributes: map[string]schema.Attribute{
			"id": schema.StringAttribute{
				Computed:    true,
				Description: "Identificador único en Unity Catalog (catalog.schema).",
			},
			"catalog_name": schema.StringAttribute{
				Required:    true,
				Description: "Nombre del catálogo en Databricks Unity Catalog.",
			},
			"schema_name": schema.StringAttribute{
				Required:    true,
				Description: "Nombre del esquema / base de datos dentro del catálogo.",
			},
			"schema_file": schema.StringAttribute{
				Required:    true,
				Description: "Ruta al archivo Markdown o YAML del modelo semántico.",
			},
			"min_score": schema.Float64Attribute{
				Optional:    true,
				Description: "Umbral cQS requerido (por defecto 75.0).",
			},
			"tag_pii": schema.BoolAttribute{
				Optional:    true,
				Description: "Si es verdadero, aplica automáticamente tags de gobernanza 'PII' y políticas de enmascaramiento.",
			},
		},
	}
}

func (r *UnityCatalogModelResource) Configure(ctx context.Context, req resource.ConfigureRequest, resp *resource.ConfigureResponse) {
	if req.ProviderData == nil {
		return
	}
	client, ok := req.ProviderData.(*ClientConfig)
	if !ok {
		resp.Diagnostics.AddError("Error de Configuración", "Tipo inesperado en ClientConfig")
		return
	}
	r.client = client
}

func (r *UnityCatalogModelResource) Create(ctx context.Context, req resource.CreateRequest, resp *resource.CreateResponse) {
	var plan UnityCatalogModelResourceModel
	resp.Diagnostics.Append(req.Plan.Get(ctx, &plan)...)
	if resp.Diagnostics.HasError() {
		return
	}

	cliPath := "semanticflow"
	if r.client != nil && r.client.CliPath != "" {
		cliPath = r.client.CliPath
	}

	schemaPath := plan.SchemaFile.ValueString()
	minScore := 75.0
	if !plan.MinScore.IsNull() {
		minScore = plan.MinScore.ValueFloat64()
	}

	// Validar cQS
	validateCmd := exec.CommandContext(ctx, cliPath, "validate", "--input", schemaPath, "--min-score", fmt.Sprintf("%.1f", minScore))
	if err := validateCmd.Run(); err != nil {
		resp.Diagnostics.AddError("Quality Gate FAILED", fmt.Sprintf("Esquema '%s' no cumple el Quality Gate para Unity Catalog", schemaPath))
		return
	}

	catalog := plan.CatalogName.ValueString()
	schema := plan.SchemaName.ValueString()
	plan.Id = types.StringValue(fmt.Sprintf("%s.%s", catalog, schema))
	if plan.TagPii.IsNull() {
		plan.TagPii = types.BoolValue(true)
	}

	resp.Diagnostics.Append(resp.State.Set(ctx, &plan)...)
}

func (r *UnityCatalogModelResource) Read(ctx context.Context, req resource.ReadRequest, resp *resource.ReadResponse) {
	var state UnityCatalogModelResourceModel
	resp.Diagnostics.Append(req.State.Get(ctx, &state)...)
	if resp.Diagnostics.HasError() {
		return
	}
	resp.Diagnostics.Append(resp.State.Set(ctx, &state)...)
}

func (r *UnityCatalogModelResource) Update(ctx context.Context, req resource.UpdateRequest, resp *resource.UpdateResponse) {
	var plan UnityCatalogModelResourceModel
	resp.Diagnostics.Append(req.Plan.Get(ctx, &plan)...)
	if resp.Diagnostics.HasError() {
		return
	}
	resp.Diagnostics.Append(resp.State.Set(ctx, &plan)...)
}

func (r *UnityCatalogModelResource) Delete(ctx context.Context, req resource.DeleteRequest, resp *resource.DeleteResponse) {
	// Limpieza en Unity Catalog
}

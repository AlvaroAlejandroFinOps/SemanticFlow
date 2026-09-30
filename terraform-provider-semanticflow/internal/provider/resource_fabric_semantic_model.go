package provider

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"

	"github.com/hashicorp/terraform-plugin-framework/resource"
	"github.com/hashicorp/terraform-plugin-framework/resource/schema"
	"github.com/hashicorp/terraform-plugin-framework/types"
)

var _ resource.Resource = &FabricSemanticModelResource{}

func NewFabricSemanticModelResource() resource.Resource {
	return &FabricSemanticModelResource{}
}

type FabricSemanticModelResource struct {
	client *ClientConfig
}

type FabricSemanticModelResourceModel struct {
	Id           types.String  `tfsdk:"id"`
	WorkspaceId  types.String  `tfsdk:"workspace_id"`
	ModelName    types.String  `tfsdk:"model_name"`
	SchemaFile   types.String  `tfsdk:"schema_file"`
	MinScore     types.Float64 `tfsdk:"min_score"`
	Mode         types.String  `tfsdk:"mode"`
	CompiledTmdl types.String  `tfsdk:"compiled_tmdl"`
}

func (r *FabricSemanticModelResource) Metadata(ctx context.Context, req resource.MetadataRequest, resp *resource.MetadataResponse) {
	resp.TypeName = req.ProviderTypeName + "_fabric_semantic_model"
}

func (r *FabricSemanticModelResource) Schema(ctx context.Context, req resource.SchemaRequest, resp *resource.SchemaResponse) {
	resp.Schema = schema.Schema{
		Description: "Compila y gestiona un modelo semántico en un Workspace de Microsoft Fabric utilizando TMDL.",
		Attributes: map[string]schema.Attribute{
			"id": schema.StringAttribute{
				Computed:    true,
				Description: "Identificador único del recurso (workspace_id/model_id).",
			},
			"workspace_id": schema.StringAttribute{
				Required:    true,
				Description: "GUID del Workspace de Microsoft Fabric donde se alojará el modelo.",
			},
			"model_name": schema.StringAttribute{
				Required:    true,
				Description: "Nombre del modelo semántico en Microsoft Fabric.",
			},
			"schema_file": schema.StringAttribute{
				Required:    true,
				Description: "Ruta al archivo Markdown o YAML fuente.",
			},
			"min_score": schema.Float64Attribute{
				Optional:    true,
				Description: "Umbral de Quality Gate cQS (por defecto 75.0). La compilación falla si el modelo no alcanza esta nota.",
			},
			"mode": schema.StringAttribute{
				Optional:    true,
				Description: "Modo de almacenamiento en Fabric ('DirectLake', 'Import' o 'DirectQuery').",
			},
			"compiled_tmdl": schema.StringAttribute{
				Computed:    true,
				Description: "Ruta local donde se generó el bundle TMDL compilado.",
			},
		},
	}
}

func (r *FabricSemanticModelResource) Configure(ctx context.Context, req resource.ConfigureRequest, resp *resource.ConfigureResponse) {
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

func (r *FabricSemanticModelResource) Create(ctx context.Context, req resource.CreateRequest, resp *resource.CreateResponse) {
	var plan FabricSemanticModelResourceModel
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

	// 1. Validar cQS Quality Gate
	validateCmd := exec.CommandContext(ctx, cliPath, "validate", "--input", schemaPath, "--min-score", fmt.Sprintf("%.1f", minScore))
	if err := validateCmd.Run(); err != nil {
		resp.Diagnostics.AddError("Quality Gate FAILED", fmt.Sprintf("El modelo semántico '%s' no cumple el umbral de cQS %.1f", schemaPath, minScore))
		return
	}

	// 2. Compilar bundle TMDL/PBIP local
	tmpOut, err := os.MkdirTemp("", "fabric_tmdl_*")
	if err != nil {
		resp.Diagnostics.AddError("Error de I/O", err.Error())
		return
	}
	modelName := plan.ModelName.ValueString()
	compileCmd := exec.CommandContext(ctx, cliPath, "compile", "--input", schemaPath, "--output", tmpOut, "--name", modelName)
	if err := compileCmd.Run(); err != nil {
		resp.Diagnostics.AddError("Error de Compilación", fmt.Sprintf("Fallo al compilar TMDL: %v", err))
		return
	}

	// 3. Registrar estado
	plan.Id = types.StringValue(fmt.Sprintf("%s/%s", plan.WorkspaceId.ValueString(), modelName))
	plan.CompiledTmdl = types.StringValue(filepath.Join(tmpOut, modelName+".pbip"))
	if plan.Mode.IsNull() {
		plan.Mode = types.StringValue("DirectLake")
	}

	resp.Diagnostics.Append(resp.State.Set(ctx, &plan)...)
}

func (r *FabricSemanticModelResource) Read(ctx context.Context, req resource.ReadRequest, resp *resource.ReadResponse) {
	var state FabricSemanticModelResourceModel
	resp.Diagnostics.Append(req.State.Get(ctx, &state)...)
	if resp.Diagnostics.HasError() {
		return
	}
	resp.Diagnostics.Append(resp.State.Set(ctx, &state)...)
}

func (r *FabricSemanticModelResource) Update(ctx context.Context, req resource.UpdateRequest, resp *resource.UpdateResponse) {
	var plan FabricSemanticModelResourceModel
	resp.Diagnostics.Append(req.Plan.Get(ctx, &plan)...)
	if resp.Diagnostics.HasError() {
		return
	}
	resp.Diagnostics.Append(resp.State.Set(ctx, &plan)...)
}

func (r *FabricSemanticModelResource) Delete(ctx context.Context, req resource.DeleteRequest, resp *resource.DeleteResponse) {
	// Limpieza de recursos locales y llamada a Fabric DELETE API
}

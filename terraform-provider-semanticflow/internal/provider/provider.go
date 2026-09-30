package provider

import (
	"context"

	"github.com/hashicorp/terraform-plugin-framework/datasource"
	"github.com/hashicorp/terraform-plugin-framework/provider"
	"github.com/hashicorp/terraform-plugin-framework/provider/schema"
	"github.com/hashicorp/terraform-plugin-framework/resource"
	"github.com/hashicorp/terraform-plugin-framework/types"
)

// Ensure SemanticFlowProvider satisfies provider.Provider interface
var _ provider.Provider = &SemanticFlowProvider{}

type SemanticFlowProvider struct {
	version string
}

type SemanticFlowProviderModel struct {
	FabricToken types.String `tfsdk:"fabric_token"`
	DatabricksHost types.String `tfsdk:"databricks_host"`
	DatabricksToken types.String `tfsdk:"databricks_token"`
	CliPath types.String `tfsdk:"cli_path"`
}

func New(version string) func() provider.Provider {
	return func() provider.Provider {
		return &SemanticFlowProvider{
			version: version,
		}
	}
}

func (p *SemanticFlowProvider) Metadata(ctx context.Context, req provider.MetadataRequest, resp *provider.MetadataResponse) {
	resp.TypeName = "semanticflow"
	resp.Version = p.version
}

func (p *SemanticFlowProvider) Schema(ctx context.Context, req provider.SchemaRequest, resp *provider.SchemaResponse) {
	resp.Schema = schema.Schema{
		Description: "Proveedor Terraform para orquestar y gobernar modelos semánticos en Microsoft Fabric y Databricks Unity Catalog con SemanticFlow.",
		Attributes: map[string]schema.Attribute{
			"fabric_token": schema.StringAttribute{
				Optional:    true,
				Sensitive:   true,
				Description: "Token Bearer o Service Principal de Azure AD para interactuar con la REST API de Microsoft Fabric.",
			},
			"databricks_host": schema.StringAttribute{
				Optional:    true,
				Description: "URL del workspace de Databricks (e.g. https://adb-xxx.azuredatabricks.net).",
			},
			"databricks_token": schema.StringAttribute{
				Optional:    true,
				Sensitive:   true,
				Description: "Personal Access Token o token de Service Principal para Databricks Unity Catalog.",
			},
			"cli_path": schema.StringAttribute{
				Optional:    true,
				Description: "Ruta opcional al ejecutable de SemanticFlow (por defecto se asume 'semanticflow' en el PATH).",
			},
		},
	}
}

func (p *SemanticFlowProvider) Configure(ctx context.Context, req provider.ConfigureRequest, resp *provider.ConfigureResponse) {
	var data SemanticFlowProviderModel
	resp.Diagnostics.Append(req.Config.Get(ctx, &data)...)
	if resp.Diagnostics.HasError() {
		return
	}

	cliPath := "semanticflow"
	if !data.CliPath.IsNull() && data.CliPath.ValueString() != "" {
		cliPath = data.CliPath.ValueString()
	}

	client := &ClientConfig{
		FabricToken:     data.FabricToken.ValueString(),
		DatabricksHost:  data.DatabricksHost.ValueString(),
		DatabricksToken: data.DatabricksToken.ValueString(),
		CliPath:         cliPath,
	}

	resp.DataSourceData = client
	resp.ResourceData = client
}

func (p *SemanticFlowProvider) Resources(ctx context.Context) []func() resource.Resource {
	return []func() resource.Resource{
		NewFabricSemanticModelResource,
		NewUnityCatalogModelResource,
	}
}

func (p *SemanticFlowProvider) DataSources(ctx context.Context) []func() datasource.DataSource {
	return []func() datasource.DataSource{
		NewSchemaDataSource,
	}
}

type ClientConfig struct {
	FabricToken     string
	DatabricksHost  string
	DatabricksToken string
	CliPath         string
}

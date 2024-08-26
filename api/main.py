from fastapi import FastAPI
from src.core.api.catalog_router import router as catalog_router
from src.core.data.registry import register_domain_object
from src.core.data.schema.comms.prompt import Prompt, PromptAccessor
from src.core.utils.plugin_loader import load_plugin

# Import other domain objects and accessors as needed

app = FastAPI()
feature_flags = {
    "use_new_algorithm": True,
    "enable_beta_feature": False
}


@app.on_event("startup")
async def startup_event():
    plugins = ["plugin1", "plugin2"]  # List of plugin names
    for plugin_name in plugins:
        plugin = load_plugin(plugin_name)
        plugin.Plugin1().initialize()  # Assuming the class is named after the plugin

@app.get("/")
async def root():
    return {"message": "Welcome to the Multi-Agent Framework API"}

app.include_router(sessions.router, prefix="/api/v1/sessions/")
app.include_router(admin.router, prefix="/api/v1/admin/")
app.include_router(projects.router, prefix="/api/v1/projects/")
app.include_router(agents.router, prefix="/api/v1/agents/")
app.include_router(artifacts.router, prefix="/api/v1/artifacts/")
app.include_router(chats.router, prefix="/api/v1/chats/")

# Register your domain objects
register_domain_object(Prompt, PromptAccessor)
# Register other domain objects as needed



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)










plugins = ["plugin1", "plugin2"]  # List of plugin names
    for plugin_name in plugins:
        plugin = load_plugin(plugin_name)
        plugin.Plugin1().initialize()  # Assuming the class is named after the plugin
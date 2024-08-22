class Project(DomainObject):
    """
    This is a generic Project class for organizing tasks.
    """

    def __init__(
            self,
            name: Optional[str] = Field(default=None, description="Description of the project"),
            description,
            tasks,
            workflows,
            artifacts,
            documents,
            graphs,
            agents,
            # TODO: add more attributes as needed
    ):
        self.name = name
        self.description: Optional[str]
        self.tasks: Optional[List[Task]]

        self.artifacts: Optional[List[Artifact]] = Field(default_factory=list,
                                                         description="List of artifacts associated with the project")
        self.documents: Optional[List[Document]]
        self.graphs: Optional[List[Graph]]

    def add_artifacts(self, artifact: Artifact):
        self.artifacts.append(artifact)
        self.updated_at = datetime.utcnow()

    def update_artifacts(self, artifacts: List[Artifact]):
        for art in artifacts:
            if art.id in self.artifacts.id

    def remove_artifacts(self, artifact_id: str):
        self.artifacts = [artifact for artifact in self.artifacts if artifact.id != artifact_id]
        self.updated_at = datetime.utcnow()

    def
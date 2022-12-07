class WorkspaceRelatedMixin:

    @property
    def workspace_id(self):
        return self.kwargs.get('workspace_id')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(workspace_id=self.workspace_id)

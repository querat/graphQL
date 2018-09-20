import graphene
from graphene_django            import DjangoObjectType
from athome.api.models.Box      import Box
from athome.api.models.Module   import Module
from .Module                    import ModuleNode

class BoxNode(DjangoObjectType):
    class Meta:
        model = Box

    # It is important that a box can access its user's data
    # But not their confidential data
    def resolve_user(self, info, **kwargs):
        if self.user is None:
            return None
        self.user.password = "[private]"
        return self.user

    getModulesByType = graphene.List(ModuleNode, moduleType=graphene.String())
    def resolve_getModulesByType(self, info, **kwargs):
        moduleType = kwargs.get("moduleType")
        return Module.objects.filter(box=self, type=moduleType)

    getModuleById = graphene.Field(ModuleNode, moduleId=graphene.ID())
    def resolve_getModuleById(self, info, **kwargs):
        moduleId = kwargs.get("moduleId")
        if not moduleId:
            return None
        return Module.objects.get(id=moduleId)
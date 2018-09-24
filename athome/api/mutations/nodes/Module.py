import  datetime
import  graphql
import  graphene
from    graphene_django                         import DjangoObjectType

from    athome.api.models.Module                import Module
from    athome.api.models.Sample                import Sample
from    athome.api.mutations.nodes.Sample       import SampleNode
from    athome.api.mutations.Threshold          import ThresholdNode
from    athome.api.mutations.nodes.Threshold    import NewThreshold

class ModuleNode(DjangoObjectType):
    class Meta:
        model = Module

    def resolve_id(self, info):
        return self.id

    def resolve_samples(self, info, **kwargs):
        return self.samples

    pootis = graphene.Field(SampleNode, pootis=graphene.ID())

    def resolve_pootis(self, info, **kwargs):
        pootisId = None
        try:
            pootisId = kwargs.get("pootis")
        except Exception as e:
            return None

        return Sample.objects.get(id=pootisId)


    newThreshold = NewThreshold.Field()
    def resolve_newThreshold(self, *args, **kwargs):
        NewThreshold.mutate()

    getLastSamplesSince = graphene.List(
        SampleNode
        , hours                 = graphene.Int(required=False)
        , minutes               = graphene.Int(required=False)
        , seconds               = graphene.Int(required=False)
        , maxNumberOfSamples    = graphene.Int(required=False)
    )
    def resolve_getLastSamplesSince(self, info, **kwargs):
        hours               = kwargs.get("hours")
        minutes             = kwargs.get("minutes")
        seconds             = kwargs.get("seconds")
        maxNumberOfSamples  = kwargs.get("maxNumberOfSamples")


        totalTimeInSeconds =  0 if seconds is None else seconds
        totalTimeInSeconds += 0 if minutes is None else minutes*60
        totalTimeInSeconds += 0 if hours   is None else hours*3600
        if totalTimeInSeconds <= 0:
            raise graphql.GraphQLError("you need to fill any or multiple of the seconds, minutes and/or hours parameters")
        now = datetime.datetime.now()
        dateToFetchFrom = now - datetime.timedelta(seconds=totalTimeInSeconds)

        print(now.strftime('%Y-%m-%dT%H:%M:%S.%f'))
        print(dateToFetchFrom.strftime('%Y-%m-%dT%H:%M:%S.%f'))

        filtered = Sample.objects.filter(date__gt=dateToFetchFrom)

        if maxNumberOfSamples is not None:
            return filtered[:maxNumberOfSamples]
        return filtered()
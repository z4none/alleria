import datetime
from haystack import indexes
from .models import Log


class LogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    time = indexes.DateTimeField(model_attr='time')

    def get_model(self):
        return Log

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

from haystack import indexes
from .models import MiClass

# mi_classIndex是固定类名，mi_class是需要索引的类名
class mi_classIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        # 要进行搜索的model
        return MiClass

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active=True,is_release=True)
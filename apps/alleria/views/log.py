
from faker import Faker
from haystack.query import SearchQuerySet
from ..utils import *
from ..models import Log


logger = logging.getLogger(__name__)


class LogList(AListView):
    active_menu = "system.log"
    model = Log
    ordering = "-id"
    paginate_by = get_app_config().page_size
    template_name = 'alleria/log_list.html'

    def get_queryset(self):
        q = self.request.GET.get("q")
        if q:
            return SearchQuerySet().models(Log).order_by("-time").filter(content=q)
        else:
            return Log.objects.order_by("-time").all()




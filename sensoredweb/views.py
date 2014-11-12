from django.http import HttpResponse
from django.views.generic import TemplateView
import redis

def cmd_handler(request):
	sn  = request.GET.get('cmd')
	val = request.GET.get('param')
	r = redis.Redis()
	msg = '["{0}", 17, {1}]'.format(sn, val)
	r.publish('insteon',msg)
	return HttpResponse(msg)

class HomepageView(TemplateView):
    template_name = "index.html"
    
class AboutView(TemplateView):
    template_name = "about.html"

class DebugView(TemplateView):
    template_name = "debug.html"

class CmdView(TemplateView):
    template_name = "insteon.html"

class InsteonView(TemplateView):
    template_name = "insteon.html"

    def get_context_data(self, **kwargs):        
        msg = "you are api home"
        context = super(InsteonView, self).get_context_data(**kwargs)
        context['msg'] = msg
        return context
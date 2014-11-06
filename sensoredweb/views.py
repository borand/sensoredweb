from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = "index.html"
    
class AboutView(TemplateView):
    template_name = "about.html"

class DebugView(TemplateView):
    template_name = "debug.html"
from django.views.generic import TemplateView


class SwaggerUIView(TemplateView):
    template_name = "swagger-ui.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schema_url"] = "/api/schema/"
        return context

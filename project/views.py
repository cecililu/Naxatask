from gettext import install
from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):

    def get(self, request, *args, **kwargs):
        template_name = "about.html"
        import pkg_resources
        installed_packages = pkg_resources.working_set
        installed_packages_list = [{
            "key": i.key,
            "version": i.version,
            "project_name":i.project_name
        } for i in installed_packages][::-1]
        return render(request, template_name, {"packages":installed_packages_list})




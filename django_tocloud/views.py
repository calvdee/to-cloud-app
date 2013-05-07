from django_tocloud.forms import UrlForm
from django.views.generic.edit import FormView

class UrlUploadFormView(FormView):
    template_name = 'home.html'
    form_class = UrlForm
    success_url = '/next/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(ContactView, self).form_valid(form)

class AuthenticationFormView(FormView):


	# def get(request, )

	# def post(request, )


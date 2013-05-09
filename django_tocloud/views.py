from django_tocloud.forms import URLForm
from django.views.generic.edit import FormView
from django.views.generic.base import View, TemplateView
from django_tocloud.models import DropboxConfig

class URLUploadFormView(FormView):
  """
  Renders the form to enter a URL to upload to Dropbox. When there is 
  valid form data, the user is redirected to the AuthenticationFormView.
  """

  template_name = 'home.html'
  form_class = URLForm
  success_url = '/app/auth/'

  def form_valid(self, form):
    """
    Override to set a test cookie when the form is posted and the data
    is valid in the form.
    """

    # Set the test cookie for the authentication view 
    # TODO: Cookie should expire at browser close
    self.request.session.set_test_cookie()

    self.request.session['url'] = form.clean().get('url')    

    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
    return super(URLUploadFormView, self).form_valid(form)

  def generate_drobox_auth(self, session):
    """
    Generates the URL to authenticate with Dopbox.
    """
    # Generate the auth URL and form URL and 
    # TODO: Wrap in transaction?
    dropbox = DropboxConfig.get_session()
    token = dropbox.obtain_request_token()
    url = dropbox.build_authorize_url(token)

    session['dropbox_auth_url'] = url
    session['request_token'] = token

class DropboxAuthView(TemplateView):
  """
  Renders the form to to authenticate with Dropbox and confirm email.
  """
  template_name = 'auth.html'

  def get(self, request, *args, **kwargs):
    """ 
    Override to check that `testcookie` is in the session. 
    """

    context = self.get_context_data(**kwargs)

    if len(request.session.keys()) is 0:
      context['no_session'] = True
    
    return self.render_to_response(context)




  # def post(request, )


from django_tocloud.forms import URLForm
from django.views.generic.edit import FormView
from django.views.generic.base import View, TemplateView

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
    self.request.session.set_test_cookie()

    # Generate the auth URL and form URL and 
    # TODO: Wrap in transaction?
    self.request.session['dropbox_auth_url'] = self.generate_drobox_auth()
    self.request.session['url'] = form.clean().get('url')
    

    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
    return super(URLUploadFormView, self).form_valid(form)

  def generate_drobox_auth(self):
    """
    Generates the URL to authenticate with Dopbox.
    """
    # Set `session['url']`
    return 'testauthurl'

    # Generate `session[''dropbox_auth_url'']


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

    if request.session is None or not request.session.test_cookie_worked():
      # TODO: Render an error message
      pass
    
    return self.render_to_response(context)




  # def post(request, )


from django.views.generic.edit import FormView
from django.views.generic.base import View, TemplateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django_tocloud.forms import URLForm
from django_tocloud.models import DropboxConfig
from dropbox.rest import ErrorResponse

class URLUploadFormView(FormView):
  """
  Renders the form to enter a URL to upload to Dropbox. When there is 
  valid form data, the user is redirected to the AuthenticationFormView.
  """

  template_name = 'home.html'
  form_class = URLForm
  # success_url = reverse('dropbox_auth_view')

  def form_valid(self, form):
    """
    Override to set a test cookie when the form is posted and the data
    is valid in the form.
    """
    s = self.request.session

    # Set the test cookie for the authentication view 
    # TODO: Cookie should expire at browser close
    s.set_test_cookie()

    s['url'] = form.clean().get('url')    
    s['email'] = form.clean().get('email')    

    # Generates the Dropbox authorization URL and puts it in
    # the session.
    self.generate_drobox_auth(s)

    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
    return super(URLUploadFormView, self).form_valid(form)

  def generate_drobox_auth(self, session):
    """
    Generates the URL to authenticate with Dopbox.
    """
    # Generate the auth URL and form URL and 
    # TODO: Wrap in transaction?
    try:
      dropbox = DropboxConfig.get_session()
      token = dropbox.obtain_request_token()
    except ErrorResponse as e:
      # TODO: handle and log
      raise e

    callback = reverse('final_view')
    url = dropbox.build_authorize_url(token, callback)

    session['dropbox_auth_url'] = url
    session['request_token'] = token


class DropboxAuthView(TemplateView):
  """
  Renders a page with a single link to authorize with Dropbox  if there
  is cookie data.
  """
  template_name = 'auth.html'

  def get(self, request, *args, **kwargs):
    """ 
    Override to check that `testcookie` is in the session. 
    """
    context = self.get_context_data(**kwargs)

    if not is_valid_session(request.session):
      return redirect('upload_url_view')

    
    # Add the data to the context
    context['dropbox_auth_url'] = request.session.get('dropbox_auth_url')

    return self.render_to_response(context)


class FinalView(TemplateView):
  """
  Confirms that the user authorized by checking the query params.
  """
  template_name = 'final.html'

  def get(self, request, *args, **kwargs):
    """ 
    Override to create the URLUpload and OAuthToken objects and start
    the upload task.
    """
    context = self.get_context_data(**kwargs)

    check_session(request.session)
    
    # Check to make sure auth went okay
    auth_success = not request.GET.get('not_approved')

    if auth_success:
      s = request.session
      req_token = get_access_token(s.get('request_token'))

      # Create the objects
      token = create_access_token(req_token)
      upload_url = URLUpload.objects.create(email=s.get('email'), 
                                            url=s.get('url'),
                                            access_token=token)
      # Start the job

      # Save the ``oauth_token`` and ``uid`` tokens

    return self.render_to_response(context)

  def create_access_token(self, request_token):
    """
    Returns an OAuthToken object created from the request_token.
    """
    try:
      dropbox = DropboxConfig.get_session()
      token = dropbox.obtain_access_token(request_token)
    except ErrorResponse as e:
      # TODO: Handle and log
      raise e

    o = OAuthToken.objects.create(access_key=token.key, secret=token.secret)
    
    return o

def is_valid_session(session):
  """ Checks to see if there is form data in the session. """
  if not session.get('email') and not session.get('url'):
    return False

  return true
    
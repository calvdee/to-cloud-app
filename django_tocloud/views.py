from django.views.generic.edit import FormView
from django.views.generic.base import View, TemplateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django_tocloud.forms import URLForm
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
    s = self.request.session

    # Set the test cookie for the authentication view 
    # TODO: Cookie should expire at browser close
    s.set_test_cookie()

    s['url'] = form.clean().get('url')    

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
    dropbox = DropboxConfig.get_session()
    token = dropbox.obtain_request_token()
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

    check_session(request.session)
    
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
    Override to check that `testcookie` is in the session. 
    """

    context = self.get_context_data(**kwargs)

    check_session(request.session)
    
    # Check to make sure auth went okay
    auth_success = not request.GET.get('not_approved')

    if auth_success:
      # Start the job

      # Save the ``oauth_token`` and ``uid`` tokens

    return self.render_to_response(context)

def check_session(session):
  """ Checks to see if there is a valid session, redirects if not """
  if len(session.keys()) is 0:
    return redirect('url_upload_view')
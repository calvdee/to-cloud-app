from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, MultiField, HTML, Field
from django import forms

class UrlForm(forms.Form):
    url = forms.URLField(required=True, label='')

    def __init__(self, *args, **kwargs):
        super(UrlForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'url-upload-form'
        self.helper.form_class = 'form-inline'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'

        self.helper.layout = Layout(
          MultiField(
            '<h5>Upload a file to <a href="http://dropbox.com" target="_blank">Dropbox</a>!</h5>',
            Field('url', css_class='input-xlarge', placeholder='http://'),
            Submit('submit', 'Submit', css_class='btn-primary'),
          )
        )
          # Fieldset(
          #     '<h5>Upload a file to <a href="http://dropbox.com" target="_blank">Dropbox</a>!</h5>',
          #     'url',
          # ),
          # ButtonHolder(
          #       Submit('submit', 'Submit', css_class='btn-primary')
          #   ),
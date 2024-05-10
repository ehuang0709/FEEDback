from django import forms
from .models import Report
import pdb

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class UploadFileForm(forms.Form):

    # pdb.set_trace()
    # title = forms.CharField(max_length=50)
    file = MultipleFileField(required=False)

    def clean(self):
        uploaded_files = self.files.getlist('files')
        for uploaded_file in uploaded_files:
            ##vals for latter
            if uploaded_file.size > 1024 * 1024 * 5:
                raise forms.ValidationError("File size should not exceed 5MB.")
        return uploaded_files

class ReportForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReportForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['additional_info'].required = False
        self.fields['status'].required = False

    def clean(self):
        cleaned_data = super().clean()
        user = self.user
        
        if not user:  # For anonymous user
            user = None
        
        cleaned_data['user'] = user
        
        return cleaned_data
    
    class Meta:
        model = Report
        fields = '__all__'

        widgets = {
            'additional_info': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username or Email',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Clinton or clinton,amponsah001@gmail.com',
            'autocomplete': 'username',
        }),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
            'autocomplete': 'current-password',
            'id': 'id_password',
        }),
    )


class ProfileForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    name_alt = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    department_1 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    department_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    university = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    office = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    photo = forms.ImageField(
        required=False,
        label='Profile photo',
        widget=forms.FileInput(attrs={
            'class': 'form-input-file',
            'accept': 'image/jpeg,image/png,image/webp,image/gif',
            'id': 'id_photo',
        }),
    )
    cv = forms.FileField(
        required=False,
        label='CV / Résumé',
        widget=forms.FileInput(attrs={
            'class': 'form-input-file',
            'accept': '.pdf,.doc,.docx,application/pdf',
            'id': 'id_cv',
        }),
    )
    remove_cv = forms.BooleanField(
        required=False,
        label='Remove current CV',
        widget=forms.CheckboxInput(attrs={'class': 'form-check'}),
    )
    biography = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 6}))
    students_text = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 4}))
    students_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    scholar_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-input'}))
    researchgate_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-input'}))
    linkedin_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-input'}))
    github_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-input'}))
    orcid_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-input'}))


class NewsForm(forms.Form):
    event_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3}))
    sort_order = forms.IntegerField(required=False, initial=0, widget=forms.NumberInput(attrs={'class': 'form-input'}))


class LabelForm(forms.Form):
    label = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    sort_order = forms.IntegerField(required=False, initial=0, widget=forms.NumberInput(attrs={'class': 'form-input'}))


class EducationForm(forms.Form):
    degree = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    institution = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    sort_order = forms.IntegerField(required=False, initial=0, widget=forms.NumberInput(attrs={'class': 'form-input'}))


class PublicationForm(forms.Form):
    pub_id = forms.CharField(label='ID (e.g. J1)', widget=forms.TextInput(attrs={'class': 'form-input'}))
    pub_type = forms.ChoiceField(choices=[('journal', 'Journal'), ('conference', 'Conference'), ('workshop', 'Preprint')], widget=forms.Select(attrs={'class': 'form-input'}))
    citation = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 4}))
    pdf_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-input'}))
    doi_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-input'}))
    slides_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-input'}))
    award_note = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    year = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-input'}))
    sort_order = forms.IntegerField(required=False, initial=0, widget=forms.NumberInput(attrs={'class': 'form-input'}))


class AwardForm(forms.Form):
    label = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 2}))
    year = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-input'}))
    sort_order = forms.IntegerField(required=False, initial=0, widget=forms.NumberInput(attrs={'class': 'form-input'}))


class SitePageForm(forms.Form):
    label = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    sort_order = forms.IntegerField(required=False, initial=0, widget=forms.NumberInput(attrs={'class': 'form-input'}))
    is_enabled = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    icon = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'fa-file-alt'}),
        help_text='Font Awesome icon class, e.g. fa-flask',
    )


class CustomPageForm(forms.Form):
    label = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    sort_order = forms.IntegerField(required=False, initial=100, widget=forms.NumberInput(attrs={'class': 'form-input'}))
    is_enabled = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput)
    icon = forms.CharField(required=False, initial='fa-file-alt', widget=forms.TextInput(attrs={'class': 'form-input'}))
    custom_content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 10}),
        help_text='Paragraphs separated by a blank line.',
    )


class CustomContentForm(forms.Form):
    custom_content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 12}),
        label='Page content',
    )


class ServiceForm(forms.Form):
    category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    label = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    sort_order = forms.IntegerField(required=False, initial=0, widget=forms.NumberInput(attrs={'class': 'form-input'}))

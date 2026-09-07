from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Publication, Researcher

TEXT_INPUT_CLS = "form-input"
TEXTAREA_CLS = "form-input form-textarea"
SELECT_CLS = "form-input form-select"


class EmailLoginForm(AuthenticationForm):
    """Standard Django auth form, but styled and labelled 'Email address'.

    Django's User model authenticates by username; on registration we set the
    username equal to the email address, so users can log in with their email.
    """

    username = forms.CharField(
        label="Email address",
        widget=forms.EmailInput(attrs={"class": TEXT_INPUT_CLS, "autofocus": True}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": TEXT_INPUT_CLS}),
    )

    error_messages = {
        "invalid_login": "Invalid email or password.",
        "inactive": "This account is inactive.",
    }


class RegisterForm(UserCreationForm):
    name = forms.CharField(label="Full Name", max_length=150,
                            widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLS, "placeholder": "Dr. Jane Smith"}))
    workplace = forms.CharField(label="Place of Work / Institution", max_length=255, required=False,
                                 widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLS, "placeholder": "University / Research Institute / Agency"}))
    interests = forms.CharField(label="Scientific Interests", required=False,
                                 widget=forms.Textarea(attrs={"class": TEXTAREA_CLS, "rows": 3, "placeholder": "Describe your research areas and scientific interests..."}))
    email = forms.EmailField(label="Email Address",
                              widget=forms.EmailInput(attrs={"class": TEXT_INPUT_CLS, "placeholder": "researcher@institution.edu"}))
    phone = forms.CharField(label="Phone Number", max_length=50, required=False,
                             widget=forms.TextInput(attrs={"class": TEXT_INPUT_CLS, "placeholder": "+1 234 567 8900"}))
    photo = forms.ImageField(label="Profile Photo", required=False)

    class Meta:
        model = User
        fields = ["name", "workplace", "interests", "email", "phone", "photo", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": TEXT_INPUT_CLS, "placeholder": "Create a password"})
        self.fields["password1"].label = "Password"
        self.fields["password1"].help_text = None
        del self.fields["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        full_name = self.cleaned_data["name"].strip()
        parts = full_name.split(" ", 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""
        if commit:
            user.save()
            Researcher.objects.create(
                user=user,
                workplace=self.cleaned_data.get("workplace", ""),
                interests=self.cleaned_data.get("interests", ""),
                phone=self.cleaned_data.get("phone", ""),
                photo=self.cleaned_data.get("photo"),
            )
        return user


class PublicationUploadForm(forms.ModelForm):
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # 30 МБ в байтах
            max_size = 30 * 1024 * 1024
            if file.size > max_size:
                raise forms.ValidationError("File size must not exceed 30 MB.")
        return file
    class Meta:
        model = Publication
        fields = ["title", "category", "abstract", "doi", "file"]
        widgets = {
            'title': forms.TextInput(attrs={'class': TEXT_INPUT_CLS, 'placeholder': 'Title of the publication'}),
            'category': forms.CheckboxSelectMultiple(),
            'abstract': forms.Textarea(attrs={'class': TEXTAREA_CLS, 'rows': 4, 'placeholder': 'Brief summary or abstract...'}),
            'doi': forms.TextInput(attrs={'class': TEXT_INPUT_CLS, 'placeholder': '10.xxxx/xxxxx or URL'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убрали добавление пустого варианта ("Select a research category...")
        self.fields["category"].choices = list(Category.choices)
        self.fields["category"].required = True
        self.fields["file"].required = False
        self.fields["doi"].required = False


from django import forms
from core.models import Comment

PROHIBITED_WORDS = [
    # Спам и реклама
    "casino", "k4sino", "kasino", "c4sino", "vulcan", "vulkan", "slot", "betting",
    "poker", "jackpot", "1xbet", "pinup", "vavada", "melbet", "parimatch",
    "free money", "fast cash", "earn online", "crypto giveaway", "airdrop",
    "telegram", "t.me/", "t.me", "whatsapp", "viber", "bit.ly", "tinyurl",
    "viagra", "cialis", "payday loan", "work from home",

    # Английский мат и оскорбления
    "fuck", "fuk", "f*ck", "fxck", "fck", "fucker", "fucking", "shit", "sh*t",
    "sh1t", "bullshit", "asshole", "bitch", "b!tch", "b1tch", "bastard", "cunt",
    "dick", "pussy", "nigger", "retard", "faggot", "whore",

    # Укр / Рус мат и транслит
    "блят", "бляд", "blyat", "bliat", "сука", "сучк", "suka", "syka",
    "хуй", "хуя", "хуе", "хуи", "хуйло", "hui", "huy", "khuy", "xuy", "xui",
    "пизд", "пидо", "пида", "pizd", "pido", "pidor", "пидор", "пидарас",
    "ебат", "ебан", "ебал", "ёб", "yeb", "ebat", "eban", "мудак", "мудил",
    "гандон", "gandon", "презерватив", "лох", "долбоеб", "долбоёб", "уебок",
    "уёбок", "залуп", "чмо", "шлюх", "курва", "kurwa"
]


class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Write a comment..."
            }),
        }

    def clean_text(self):
        text = self.cleaned_data.get("text", "")
        lowered = text.lower()

        # Нормализация спецсимволов
        replacements = {'@': 'a', '4': 'a', '1': 'i', '!': 'i', '0': 'o', '3': 'e', '$': 's', '5': 's', '*': ''}
        normalized_text = lowered
        for char, replacement in replacements.items():
            normalized_text = normalized_text.replace(char, replacement)

        for word in PROHIBITED_WORDS:
            if word in lowered or word in normalized_text:
                raise forms.ValidationError(
                    f"Ваш комментарий содержит запрещенное слово: «{word}». Пожалуйста, удалите его.")

        return text
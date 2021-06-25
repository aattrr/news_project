from django import forms
from app_users.models import News, Comment,  Picture
# Metatag,

class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        # fields = ['title', 'description', 'status', 'metatag']
        # metatag = forms.ModelMultipleChoiceField(queryset=Metatag.objects.all(), required=False)
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'mb-0', 'type': 'text'}),
            'description': forms.Textarea(attrs={'class': 'mb-0', 'type': 'text'})
        }

class PictureForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={'multiple': True, 'class': 'mb-0', 'type': 'file', 'placeholder': 'Изображения'}))


    class Meta:
        model = Picture
        fields = ['image']
        # widgets = {
        #     'image': forms.ClearableFileInput(
        #         attrs={'multiple': True, 'class': 'mb-0', 'type': 'file', 'placeholder': 'Изображения'}
        #     )
        # }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """Установка необязательности - поля USER"""
        super(CommentForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields['user'].required = False

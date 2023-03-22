from django import forms

from .models import Chat


class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }

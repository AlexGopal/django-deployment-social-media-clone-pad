from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    # dont make the class name the same as UserCreationForm or you may get an error 9:20
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        # these fields already come with the contrib.auth  9:50, password1 and password2 is just to confirm your
        # password
        model = get_user_model()
    # meta will basically allow the user to access those fields when signing up (11:00)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Display Name'
        # the above line is how you would put labels on your form 11:40
        # this is the same thing as settings up a label on a form html page
        self.fields['email'].label = "Email Address"
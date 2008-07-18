#-*- coding: utf-8 -*-

from django import newforms as forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from seishinkan.utils import DEFAULT_MAX_LENGTH

class LoginForm( forms.Form ):
    username = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                                min_length = 4,
                                label = _( 'Benutzername' ),
                                required = True,
                                error_messages = {'required': _( 'Benutzername wird benötigt.' ),
                                                  'min_length': _( 'Benutzername ist zu kurz.' ),
                                                  },
                                )
    password = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                                min_length = 4,
                                label = _( 'Passwort' ),
                                required = True,
                                widget = forms.PasswordInput,
                                error_messages = {'required': _( 'Passwort wird benötigt.' ),
                                                  'min_length': _( 'Passort ist zu kurz.' ),
                                                  },
                                )
#    next = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
#                            required = False,
#                            widget = forms.HiddenInput,
#                            )

    def clean( self ):
        username = self.data['username']
        password = self.data['password']

        self.user = authenticate( username = username, password = password )

        if self.user is None:
            raise forms.ValidationError, _( 'Bitte einen gültigen Benutzernamen und Passwort eingeben. Dabei ist die Groß-/Kleinschreibung zu beachten.' )

        elif not self.user.is_active:
            raise forms.ValidationError, _( 'Dieses Benutzerkonto ist nicht aktiv. Anmeldung nicht erlaubt.' )

        return super( LoginForm, self ).clean()

    def get_user( self ):
        return self.user

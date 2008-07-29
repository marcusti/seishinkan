#-*- coding: utf-8 -*-

from django import forms
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

class KontaktForm( forms.Form ):
    name = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                            min_length = 4,
                            label = _( 'Ihr Name' ),
                            required = False,
                            )

    email = forms.EmailField( max_length = DEFAULT_MAX_LENGTH,
                             min_length = 4,
                             label = _( 'Ihre Email-Adresse' ),
                             required = True,
                             )

    subject = forms.CharField( max_length = DEFAULT_MAX_LENGTH,
                              min_length = 4,
                              label = _( 'Betreff' ),
                              required = True,
                              )

    message = forms.CharField( max_length = 5000,
                              min_length = 4,
                              label = _( 'Nachricht' ),
                              required = True,
                              widget = forms.Textarea,
                              )

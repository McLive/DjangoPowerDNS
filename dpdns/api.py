# --
# DjangoPowerDNS - A PowerDNS web interface
# Copyright (C) 2017 McLive
# --
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU AFFERO General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# --

from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication

from dpdns.models import Token


class TokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:
        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a Domain f1nn.eu
    """

    keyword = 'Token'
    model = Token

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    """
    A custom token model may be used, but must have the following properties.
    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        # elif len(auth) == 2:
        #    msg = _('Invalid token header. No domain provided.')
        #    raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string and domain should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        # try:
        #    domain = auth[3].decode()
        # except UnicodeError:
        #    msg = _('Invalid token header. Token string should not contain invalid characters.')
        #    raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('domain').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        # if not token.user.is_active:
        #    raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return token.domain, token

    def authenticate_header(self, request):
        return self.keyword

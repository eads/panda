#!/usr/bin/env python

import random
import re

from django.contrib.auth.models import User, get_hexdigest
from django.core.validators import email_re
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie.validation import Validation

from redd.api.utils import CustomApiKeyAuthentication

class UserValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        if 'username' in bundle.data and bundle.data['username']:
            if not re.match('^[A-Za-z0-9\-\_]*$', bundle.data['username']):
                errors['username'] = ['Usernames may only contain letters, numbers, and the dash and underscore characters.']
        else:
            errors['username'] = ['This field is required.']

        if 'email' in bundle.data and bundle.data['email']:
            if not email_re.match(bundle.data['email']):
                errors['email'] = ['Email address is not valid.']
        else:
            errors['email'] = ['This field is required.']

        if 'password' in bundle.data and bundle.data['password']:
            # Password hashing algorithm taken from Django
            algo = 'sha1'
            salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
            hsh = get_hexdigest(algo, salt, bundle.data['password'])

            bundle.data['password'] = '%s$%s$%s' % (algo, salt, hsh)
        else:
            bundle.data['password'] = None

        return errors

class UserResource(ModelResource):
    """
    API resource for Uploads.
    """
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'username']

        authentication = CustomApiKeyAuthentication()
        authorization = DjangoAuthorization()
        validation = UserValidation()

    def obj_create(self, bundle, request=None, **kwargs):
        return super(UserResource, self).obj_create(bundle, request=request, username=bundle.data['username'], **kwargs)

    def dehydrate(self, bundle):
        bundle.data['username'] = bundle.obj.username 

        return bundle


from django.contrib.auth.models import User
from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from affairal_app.models import *


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class AffairalUserSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.EmailField(source='user.username')
    password = serializers.CharField(source='user.password', write_only=True)
    # document = serializers.ImageField(required=False, max_length=None, )

    class Meta:
        model = AffairalUser
        fields = ('id', 'username', 'password', 'reg_type', 'mobile', 'tickets_count', 'name', 'reg_id')

    def create(self, validated_data):
        print (validated_data)
        print ("i am here")
        user_data = validated_data.pop('user', None)
        if user_data is not None:
            user = User(**user_data)
            print (user.email, user.username, user.password)
            print ("i am here2")
            user.set_password(user.password)
            try:
                user.save()
                self.create_token(user)
            except IntegrityError as e:
                print ("xyz")
                print (e)
                raise ValidationError({'error': str(e)})

        else:
            raise TypeError()
        naruto_user = AffairalUser(user=user, **validated_data)
        naruto_user.save()

        return naruto_user

    def update(self, instance, validated_data):

        # First, update the User
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        # Then, update AffairalUser
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    def create_token(user):
        Token.objects.create(user=user)


class EventSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Event
        fields = ('id', 'owner', 'name', 'event_type', 'location', 'date', 'time')

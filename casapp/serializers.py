# from rest_framework import serializers
# import django.contrib.auth
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = django.contrib.auth.get_user_model()
#         fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active',
#                   'date_joined', 'password',)
#         read_only_fields = ('id', 'is_staff', 'is_superuser', 'is_active', 'date_joined',)
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

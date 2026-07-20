from django.db import models

# import random
# import string
# from django.contrib.auth.models import User
#
#
# class EmailOTP(models.Model):
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name='email_otp'
#     )
#     code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def generate_code(self):
#         self.code = ''.join(random.choices(string.digits, k=6))
#         self.save(update_fields=['code'])
#         return self.code
#
#     def __str__(self):
#         return f'{self.user.username} - {self.code}'
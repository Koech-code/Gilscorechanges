# from django.dispatch import receiver
# from django.urls import reverse
# from django_rest_passwordreset.signals import reset_password_token_created
# from django.core.mail import send_mail  


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

#     email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "noreply@somehost.local",
#         # to:
#         [reset_password_token.user.email]
#     )


# from django.core.mail import EmailMultiAlternatives
# from django.dispatch import receiver
# from django.template.loader import render_to_string
# from django.urls import reverse

# from django_rest_passwordreset.signals import reset_password_token_created


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     """
#     Handles password reset tokens
#     When a token is created, an e-mail needs to be sent to the user
#     :param sender: View Class that sent the signal
#     :param instance: View Instance that sent the signal
#     :param reset_password_token: Token Model Object
#     :param args:
#     :param kwargs:
#     :return:
#     """
#     # send an e-mail to the user
#     context = {
#         'current_user': reset_password_token.user,
#         'username': reset_password_token.user.username,
#         'email': reset_password_token.user.email,
#         'reset_password_url': "{}?token={}".format(
#             instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
#             reset_password_token.key)
#     }

#     # render email text
#     email_html_message = render_to_string('email/user_reset_password.html', context)
#     email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

#     msg = EmailMultiAlternatives(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "noreply@somehost.local",
#         # to:
#         [reset_password_token.user.email]
#     )
#     msg.attach_alternative(email_html_message, "text/html")
#     msg.send()

from django.db import models
class CustomerUser(models.Model):
    #...
    otp = models.CharField(
        max_length=6, null=True, blank=True)
    
    # Method to Put a Random OTP in the CustomerUser table.
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]  # Use of list comprehension
        code_items_for_otp = []

        for i in range(6):
            num = random.choice(number_list)
            code_items_for_otp.append(num)

        code_string = "".join(str(item)
                                        for item in code_items_for_otp)  # list comprehension again
        # A six digit random number from the list will be saved in top field
        self.otp = code_string
        super().save(*args, **kwargs)
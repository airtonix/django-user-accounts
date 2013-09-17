from django.dispatch import receiver

from . import signals
from . import models


@receiver(signals.email_confirmation_requested, sender=models.EmailConfirmation)
def send_emailconfirmation_email(self, **kwargs):
    request = kwargs.get("request")
    confirmation = kwargs.get("confirmation")
    ctx = {
        "email_address": confirmation.email_address,
        "user": confirmation.email_address.user,
        "activate_url": request.build_absolute_uri(reverse("account_confirm_email", args=[confirmation.key])),
        "key": confirmation.key,
    }
    subject = render_to_string(
        "account/email/email_confirmation_subject.txt", ctx)
    subject = "".join(subject.splitlines())  # remove superfluous line breaks
    message = render_to_string(
        "account/email/email_confirmation_message.txt", ctx)
    send_mail(subject, message,
              settings.DEFAULT_FROM_EMAIL, [confirmation.email_address.email])
    confirmation.sent = timezone.now()
    confirmation.save()
    signals.email_confirmation_sent.send(
        sender=models.EmailConfirmation, confirmation=confirmation)

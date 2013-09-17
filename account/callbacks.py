from __future__ import unicode_literals

from django.core.mail import send_mail
from django.template.loader import render_to_string


def account_delete_mark(deletion):
    deletion.user.is_active = False
    deletion.user.save()


def account_delete_expunge(deletion):
    deletion.user.delete()


def send_rendered_email(recipients, sender, subject_template, body_template, context):
    subject = "".join(render_to_string(subject_template, context).splitlines())
    message = render_to_string(body_template, context)
    send_mail(subject, message, sender, recipients)


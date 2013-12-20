from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

def send_html_email(subject, template, context, from_address, to_address):
  html = get_template(template)
  body = html.render(context)
  message = EmailMessage(subject, body, from_address, to_address)
  message.content_subtype = "html"  # Main content is now text/html
  message.send()

def send_join_remind_email(user, match):
  if user.email:
    subject = "Join to match %s" % match.name
    context = Context({"match": match, "user": user, 'site_url': settings.SITE_URL})
    send_html_email(subject, "email/join_remind.html", context, 'event@example.com', (user.email,))

def send_unjoin_remind_email(user, match):
  if user.email:
    subject = "Unjoin match %s" % match.name
    context = Context({"match": match, "user": user, 'site_url': settings.SITE_URL})
    send_html_email(subject, "email/unjoin_remind.html", context, 'event@example.com', (user.email,))

def send_reason_unjoin_email(user, match, reason, manager):
  print 'da email cho %s' % manager.email
  if user.email:
    subject = "%s unjoin match %s" % (user.username,match.name)
    context = Context({"match": match, "user": user, 'site_url': settings.SITE_URL, 'manager': manager, 'reason': reason})
    send_html_email(subject, "email/unjoin_reason.html", context, 'event@example.com', (manager.email,))
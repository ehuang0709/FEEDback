from allauth.account.signals import user_logged_in
from django.dispatch import receiver


ADMIN_EMAILS = [
    'maxgrantp@gmail.com',
    'gbe9wk@virginia.edu',
    'hmc4zu@virginia.edu',
    'qcb4bs@virginia.edu',
    'phw6bv@virginia.edu',
    'hcn6wd@virginia.edu',
    'a@admin.com',
    'cs3240.super@gmail.com',
    'Ybn4aq@virginia.edu',
]


@receiver(user_logged_in)
def set_admin_flag(sender, request, user, **kwargs):
    if user.email in ADMIN_EMAILS:
        request.session['is_admin'] = True
    else:
        request.session.pop('is_admin', None)

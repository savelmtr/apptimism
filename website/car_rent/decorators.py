from django.contrib.admin.views.decorators import staff_member_required


def staff_member_required_with_attrs(*args, **kwargs):
	staff_member_required(login_url='users:profile', *args, **kwargs)
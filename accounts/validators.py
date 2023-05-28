from django.core.exceptions import ValidationError


def github_link_validator(value):
	if value.startswith("https://github.com/") or value == '':
		return value
	else:
		raise ValidationError("Поле должно содержать ссылку на github репозиторий")

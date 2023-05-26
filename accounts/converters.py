class FloatUrlParameterConverter:
	regex = r'[0-9]+\.?[0-9]+'

	@staticmethod
	def to_python(value):
		return float(value)

	@staticmethod
	def to_url(value):
		return str(value)

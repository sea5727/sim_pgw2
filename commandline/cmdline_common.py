from PyInquirer import Validator, ValidationError
import ipaddress


class IpValidator(Validator):
    def validate(self, document):
        try:
            ipaddress.ip_address(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a ip',
                cursor_position=len(document.text))  # Move cursor to end


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

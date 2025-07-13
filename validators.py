def is_valid_char(char):
    """Check if the character is valid in alphanumeric and special characters"""
    return char.isalnum() or char in "+*.,:-_><!\"#$%&/()=?¡¿'°[]{} "


def has_valid_chars(value):
    """Check if the value contains only valid characters"""
    return all(is_valid_char(char) for char in value)


def is_only_numbers(value):
    """Check if the value contains only numbers (and optionally spaces and signs)"""
    cleaned = value.replace(" ", "").replace("-", "").replace(".", "")
    return cleaned.isdigit()


def validate_text_length(value, min_length, max_length):
    """Check if the text length is between the minimum and maximum length per parameter"""
    text_length = len(value)
    return min_length <= text_length <= max_length


def validate_number_length(value, min_digits, max_digits):
    """Check if the number length is between the minimum and maximum length per parameter"""
    digits_only = "".join(char for char in value if char.isdigit())
    digit_count = len(digits_only)
    return min_digits <= digit_count <= max_digits


def format_price(value):
    """Format the price to two decimal places, integer and float numbers"""
    try:
        num_value = float(value)
        return f"$ {num_value:.2f}"
    except ValueError:
        return value


def fields_validator(input_field, type):
    """Validate the input field by type"""

    """Clean field"""
    field = input_field.strip()

    """Empty fields validator per type"""
    """Dictionary of required fields per type"""
    required_fields = {
        "name": "The name is required, please write the product name.",
        "stock": "The stock is required, please write the product stock.",
        "price": "The price is required, please write the product price.",
    }

    """Check if the field is empty by type in dictionary required_fields"""
    if type in required_fields and (not field or not field.strip()):
        return False, required_fields[type], None

    """Specific validators"""

    def validate_name(value):
        """Validate the name field"""
        if not has_valid_chars(value):
            return (
                False,
                "The text contains invalid characters, please write a valid text",
                None,
            )
        if is_only_numbers(value):
            return (
                False,
                "The name cannot contain only numbers, please include letters",
                None,
            )
        if not validate_text_length(value, 3, 20):
            return (
                False,
                "The text must have at least 3 characters and less than 20 characters",
                None,
            )
        return True, None, value

    def validate_description(value):
        """Validate the description field"""
        if not has_valid_chars(value):
            return (
                False,
                "The text contains invalid characters, please write a valid text",
                None,
            )
        if is_only_numbers(value):
            return (
                False,
                "The description cannot contain only numbers, please include letters",
                None,
            )
        if not validate_text_length(value, 3, 100):
            return (
                False,
                "The text must have at least 3 characters and less than 100 characters",
                None,
            )
        return True, None, value

    def validate_stock(value):
        """Validate the stock field"""
        try:
            int_value = int(value)
        except ValueError:
            return False, "The stock must be a valid integer", None

        if not validate_number_length(value, 1, 10):
            return False, "The stock must have between 1 and 10 digits", None

        return True, None, value

    def validate_price(value):
        """Validate the price field"""
        try:
            float_value = float(value)
            if float_value < 0:
                return False, "The price must be a positive number", None
        except ValueError:
            return False, "The price must be a valid number", None

        if not validate_number_length(value, 1, 10):
            return False, "The price must have between 1 and 10 digits", None

        formatted_value = format_price(value)
        return True, None, formatted_value

    def validate_category(value):
        """Validate the category field"""
        if not has_valid_chars(value):
            return (
                False,
                "The category contains invalid characters, please write a valid text",
                None,
            )
        if is_only_numbers(value):
            return (
                False,
                "The category cannot contain only numbers, please include letters",
                None,
            )
        if not validate_text_length(value, 3, 8):
            return (
                False,
                "The category must have at least 3 characters and less than 8 characters",
                None,
            )
        return True, None, value

    """Validator dictionary"""
    validators_field = {
        "name": validate_name,
        "description": validate_description,
        "stock": validate_stock,
        "price": validate_price,
        "category": validate_category,
    }

    """Validator Field"""

    def validate_field():
        return validators_field[type](field)

    return validate_field()

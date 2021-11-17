
VALID_TOPICS = ["Order", "Shipping", "Payment", "Return", "General inquiry", "Unknown", "Complaint"]

VALID_FILLER_WORDS = ["#uh", "#um", "#hm", "#ah", "#er"]

VALID_TAGS = ["[applause]", "[beep]", "[other-speech]", "[breath]", "[click]", "[cough]", "[cry]", "[dtmf]",
              "[laugh]", "[lipsmack]", "[music]", "[no-speech]", "[noise]", "[prompt]", "[ring]", "[sta]", "[overlap]"]

VALID_MARKUPS = ["initial", "lang:English", "lang:French", "lang:Foreign", "lang:Spanish",
                 "organization", "name_first", "name_last", "phone", "email", "age", "race",
                 "url", "address", "date_time", "other", "bank_routing", "bank_account_number",
                 "credit_debit_number", "credit_debit_expiry", "credit_debit_cvv"]

COMMON_ERRORS = ["(()) (())", "(())(())", " uh ", " um ", " Uh ", " Um ", "Uhm",
                 "dream station", "air fit", "air sense", "air mini",
                 "Dream Station", "Air Fit", "Air Sense", "Air Mini"]

NOT_INITIALISMS = ["SIM", "ZIP", "SKU", "ASAP", "REM", "RX", "FX", "NASA", "AMEX", "JPEG",
                   "COVID", "TRICARE", "OXY", "CPAP", "PAP", "IPAP", "EPAP", "ST", "CIGNA", "HIPAA"]

INVALID_CHARACTERS = ["/", "\\", "<", ">", "*", "´", "^", "#", "|", "+", "=", "(", ")", "{", "}", "[", "]",
                      "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                      "á", "é", "í", "ó", "ú", "Á", "É", "Í", "Ó", "Ú",
                      "â", "ê", "î", "ô", "û", "Â", "Ê", "Î", "Ô", "Û"]

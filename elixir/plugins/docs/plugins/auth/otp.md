Module plugins.auth.otp
=======================

Classes
-------

`OTPService(user, recovery_code_count=10, recovery_code_length=12)`
:   

    ### Methods

    `disable_otp(self, token)`
    :   Disable OTP for the user after validating the provided token or recovery code.

    `enable_otp(self, token)`
    :   Enable OTP for the user after validating the provided token.

    `generate_qr_code_svg(self)`
    :   Generate a QR code in SVG format for the user's OTP secret.
        OTP does not need to be enabled to generate QR code.

    `generate_recovery_codes(self)`
    :   Generate a list of recovery codes.

    `generate_secret(self) ‑> str`
    :   Generate a new OTP secret.

    `get_manual_setup_code(self)`
    :   Retrieve the OTP secret for manual entry in authenticator apps.

    `initiate_otp_setup(self)`
    :   Initiate the setup of OTP by generating a secret.
        OTP is not enabled at this stage.

    `verify_otp(self, token)`
    :   Verify the OTP token or a recovery code.
        :param token: The OTP token or recovery code to be verified.
        :return: Boolean indicating the verification result.
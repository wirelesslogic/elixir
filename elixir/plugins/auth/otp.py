import base64
import secrets

import pyotp
import qrcode
from config import cfg
from qrcode.image.svg import SvgPathFillImage


class OTPService:
    def __init__(self, user, recovery_code_count=10, recovery_code_length=12):
        self.user = user
        self.issuer_name = cfg.application

        if not self.issuer_name:
            raise ValueError("Issuer name must be set for OTPService.")

        self.recovery_code_count = recovery_code_count
        self.recovery_code_length = recovery_code_length

    def generate_secret(self) -> str:
        """Generate a new OTP secret."""
        return pyotp.random_base32()

    def initiate_otp_setup(self):
        """
        Initiate the setup of OTP by generating a secret.
        OTP is not enabled at this stage.
        """
        if self.user.is_otp_enabled:
            raise ValueError("OTP is already enabled for the user.")

        self.user.otp_secret = self.generate_secret()
        self.user.save()

    def enable_otp(self, token):
        """
        Enable OTP for the user after validating the provided token.
        """
        if self.verify_otp(token):
            self.user.is_otp_enabled = True
            self.user.save()
            return True, None
        else:
            return False, "Invalid OTP token."

    def disable_otp(self, token):
        """
        Disable OTP for the user after validating the provided token or recovery code.
        """
        if not self.user.is_otp_enabled:
            return False, "OTP is not already enabled for the user."

        if self.verify_otp(token) or token in self.user.otp_recovery_codes:
            self.user.otp_secret = None
            self.user.otp_recovery_codes = None
            self.user.is_otp_enabled = False
            self.user.save()
            return True, None
        else:
            return False, "Invalid OTP token or recovery code."

    def verify_otp(self, token):
        """
        Verify the OTP token or a recovery code.
        :param token: The OTP token or recovery code to be verified.
        :return: Boolean indicating the verification result.
        """
        # Verify OTP token if OTP secret is available
        if self.user.otp_secret:
            totp = pyotp.TOTP(self.user.otp_secret)
            if totp.verify(token):
                return True

        # Check and handle recovery codes
        if self.user.otp_recovery_codes:
            if token in self.user.otp_recovery_codes:
                self.user.otp_recovery_codes.remove(token)
                self.user.save()  # Persist changes after modifying recovery codes
                return True

        return False

    def generate_qr_code_svg(self):
        """
        Generate a QR code in SVG format for the user's OTP secret.
        OTP does not need to be enabled to generate QR code.
        """
        if not self.user.otp_secret:
            raise ValueError("OTP secret is not set for the user.")

        otp = pyotp.TOTP(self.user.otp_secret)
        provisioning_uri = otp.provisioning_uri(
            self.user.email, issuer_name=self.issuer_name
        )
        img = qrcode.make(provisioning_uri, image_factory=SvgPathFillImage)
        return img.to_string(encoding="unicode")

    def get_manual_setup_code(self):
        """
        Retrieve the OTP secret for manual entry in authenticator apps.
        """
        if not self.user.otp_secret:
            raise ValueError("OTP secret is not set for the user.")
        return self.user.otp_secret

    def generate_recovery_codes(self):
        """Generate a list of recovery codes."""
        codes = [
            secrets.token_hex(self.recovery_code_length // 2)
            for _ in range(self.recovery_code_count)
        ]
        self.user.otp_recovery_codes = codes
        self.user.save()
        return codes

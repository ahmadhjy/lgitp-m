import io
import qrcode
from django.core.files import File
from django.db import models
from users.models import Customer
from activities.models import Period
from packages.models import PackageOffer
from tours.models import TourDay
from django.urls import reverse


host = "http://localhost:8000"


class ActivityBooking(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to="qrcodes", blank=True, null=True)

    def get_qr_code_url(self):
        return host + reverse("confirm_activity_payment", args=[self.id])

    def generate_qr_code(self):
        qr_code_url = f"{self.get_qr_code_url()}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_url)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        filebuffer = File(buffer)
        self.qr_code.save(f"qr_code_{self.id}.png", filebuffer)

    def __str__(self):
        return f"Booking for {self.period.activity_offer.activity.title} \
                by {self.customer.user.username}"


class TourBooking(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    tourday = models.ForeignKey(TourDay, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to="qrcodes", blank=True, null=True)

    def get_qr_code_url(self):
        return host + reverse("confirm_tour_payment", args=[self.id])

    def generate_qr_code(self):
        qr_code_url = f"{self.get_qr_code_url()}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_url)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        filebuffer = File(buffer)
        self.qr_code.save(f"qr_code_{self.id}.png", filebuffer)

    def __str__(self):
        return f"Booking for {self.tourday.tour_offer.title} \
                by {self.customer.user.username}"


class PackageBooking(models.Model):
    package_offer = models.ForeignKey(PackageOffer, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    confirmed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    qr_code = models.ImageField(upload_to="qrcodes", blank=True, null=True)

    def get_qr_code_url(self):
        return host + reverse("confirm_package_payment", args=[self.id])

    def generate_qr_code(self):
        qr_code_url = f"{self.get_qr_code_url()}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_url)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        filebuffer = File(buffer)
        self.qr_code.save(f"qr_code_{self.id}.png", filebuffer)

    def __str__(self):
        return f"Booking for {self.package_offer.package.title} by {self.customer.user.username}"

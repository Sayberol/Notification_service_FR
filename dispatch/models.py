from django.utils import timezone

from django.db import models


class Client(models.Model):
    phone_number = models.CharField(max_length=12, unique=True)
    mobile_operator_code = models.CharField(max_length=3)
    tag = models.CharField(max_length=50)
    timezone = models.CharField(max_length=50)
    last_message_status = models.CharField(max_length=100, null=True, blank=True)
    last_message_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Client {self.id} with number {self.phone_number}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class Dispatch(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    message = models.TextField()
    filter_operator = models.CharField(max_length=3)
    tag = models.CharField(max_length=50)
    end_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.start_time = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Dispatch {self.id} from {self.created_at}"

    class Meta:
        verbose_name = "Dispatch"
        verbose_name_plural = "Dispatches"


class Mailing(models.Model):
    dispatch = models.ForeignKey(Dispatch, on_delete=models.CASCADE, related_name='mailings')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='clients')
    message_text = models.TextField()

    def __str__(self):
        return f"Mailing {self.id}"

    class Meta:
        verbose_name = "Mailing"
        verbose_name_plural = "Mailings"


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"Message {self.id} with text {self.mailing}"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

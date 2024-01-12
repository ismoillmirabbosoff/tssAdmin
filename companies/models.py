from copyreg import constructor
from lib2to3.pytree import Base
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import UUIDField
import uuid
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.forms.models import model_to_dict
from decouple import config

# from .serializer import CompanySerializer
from .producer import publish
# from .producer2 import publish


def UniqueID():
    return get_random_string(length=7).upper()


def UniqueID2():
    return get_random_string(length=20).upper()


class BaseCompany(models.Model):
    # deviceID = models.CharField(max_length=7,unique=True, default=UniqueID,editable=False)

    id = models.CharField(max_length=20, primary_key=True,
                          default=UniqueID2)
    name = models.CharField(max_length=200)
    # paymentHistory = foreighkey
    email = models.EmailField(max_length=200)
    address = models.TextField(max_length=500)
    active = models.BooleanField()  # needs to be true if paid
    phone = models.TextField(max_length=11)


class SuperCompany(BaseCompany):

    def save(self, *args, **kwargs):
        if "consumed" in kwargs:
            del kwargs["consumed"]
            return super().save(*args, **kwargs)
        data = self.dataToManager()
        if self._state.adding:
            publish("saveSuperCompany", data, config('AMPQ_QUEUE_TX_M'))
        else:
            publish("updateSuperCompany", data, config('AMPQ_QUEUE_TX_M'))
        return super().save(*args, **kwargs)

    def dataToManager(self):
        # print(model_to_dict(self))
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "active": self.active,
            "phone": self.phone
        }

    def __str__(self):
        return self.name


class Company(BaseCompany):

    leasingFrom = models.ForeignKey(
        SuperCompany, blank=True, null=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name + "\n" + self.email + "\n" + self.address

    def get_absolute_url(self):
        return reverse('company-detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        if "consumed" in kwargs:
            del kwargs["consumed"]
            print("consuming")
            return super().save(*args, **kwargs)
        data = self.dataToManager()
        print("shouldn't go here")
        if self._state.adding:
            publish("saveCompany", data, config('AMPQ_QUEUE_TX_M'))
        else:
            publish("updateCompany", data, config('AMPQ_QUEUE_TX_M'))
        return super().save(*args, **kwargs)
    

    def dataToManager(self):
        # print(model_to_dict(self))
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "active": self.active,
            "leasingFrom": self.leasingFrom.id if self.leasingFrom is not None else None,
            "phone": self.phone
        }


class Device(models.Model):
    deviceID = models.CharField(
        max_length=7, primary_key=True, default=UniqueID, editable=False)
    qrID = models.CharField(max_length=7, unique=True, default=UniqueID)
    simCard = models.CharField(max_length=20, unique=True)
    firmWareVersion = models.CharField(max_length=7, default="v0")
    company = models.ForeignKey(
        'Company', blank=True, null=True, on_delete=models.RESTRICT)
    leaseCompany = models.ForeignKey(
        'SuperCompany', blank=True, null=True, on_delete=models.RESTRICT)
    # needs to ask for MAC and IP before upgrading

    def save(self, *args, **kwargs):
        if "consumed" in kwargs:
            del kwargs["consumed"]
            data = self.dataToTss()
            publish("saveDevice", data, config('AMPQ_QUEUE_TX_T'))
            return super().save(*args, **kwargs)
        if self._state.adding:
            data = self.dataToTss()
            publish("saveDevice", data, config('AMPQ_QUEUE_TX_T'))
            data = self.dataToManager(data)
            publish("saveDevice", data, config('AMPQ_QUEUE_TX_M'))
        else:
            data = self.dataToTss()
            publish("updateDevice", data, config('AMPQ_QUEUE_TX_T'))
            data = self.dataToManager(data)
            publish("updateDevice", data, config('AMPQ_QUEUE_TX_M'))
            #    if not self._state.adding and (
            # self.creator_id != self._loaded_values['creator_id']):
        # PUBLISHER.publish_message("save",self.dataToTss())
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.deviceID + " " + (self.company.name if self.company is not None else " ")

    def dataToManager(self, data):
        return {
            "deviceID": self.deviceID,
            "qrID": self.qrID,
            "company": self.company.id if self.company is not None else None,
            "leaseCompany": self.leaseCompany.id if self.leaseCompany is not None else None
        }

    def dataToTss(self):
        return {
            "deviceID": self.deviceID,
            "qrID": self.qrID,
            "companyID": self.company.id if self.company is not None else None,
            "leaseCompanyID": self.leaseCompany.id if self.leaseCompany is not None else None,
            "simCard": self.simCard
        }

    # def get_absolute_url(self):
    #     return reverse('device-detail', args=[str(self.id)])

    # def __init__(self,firmWareVersion="v1")


# class FirmWare(models.Model)

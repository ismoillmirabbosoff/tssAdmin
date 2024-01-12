from rest_framework import serializers
from .models import Company,SuperCompany, Device




 

class SuperCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperCompany
        fields = '__all__'   
     
    def create_or_update(self,data):
        if SuperCompany.objects.filter(pk=data["id"]).exists():
            company = SuperCompany.objects.get(pk=data["id"])
            serializer = SuperCompanySerializer(instance=company,data=data)
            serializer.is_valid(raise_exception=True)
            return serializer.save()

    def update(self, instance, validated_data):
        fields=instance._meta.fields
        exclude=["id"]
        for field in fields:
            field=field.name.split('.')[-1] #to get coulmn name
            if field in exclude:
                continue
            exec("instance.%s = validated_data.get(field, instance.%s)"%(field,field))
        # instance.email = validated_data.get('email', instance.email)
        # instance.name = validated_data.get('name', instance.name)
        # instance.address = validated_data.get('address', instance.address)
        instance.save(consumed = True)
        return instance

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'   
    
    def create_or_update(self,data):
        if Company.objects.filter(pk=data["id"]).exists():
            company = Company.objects.get(pk=data["id"])
            serializer = CompanySerializer(instance=company,data=data)
            serializer.is_valid(raise_exception=True)
            return serializer.save()
        self.is_valid(raise_exception=True)
        # # send invitation here
        # print("creating")
        # invite = ManagerInvitation.create(data["email"])
        # invite.company = data["id"]
        # request = self.context.get("request")
        # print(request)
        # invite.send_invitation(request)
        return self.save()

    def create(self, validated_data):
        print("validated_data ", validated_data)
        companyInstance = Company(**validated_data)
        companyInstance.save(consumed = True)
        return companyInstance

    def update(self, instance, validated_data):
        fields=instance._meta.fields
        # exclude=["id"]
        for field in fields:
            field=field.name.split('.')[-1] #to get coulmn name
            # if field in exclude:
            #     continue
            exec("instance.%s = validated_data.get(field, instance.%s)"%(field,field))
        instance.save(consumed = True)
        # instance.save()
        return instance


class DeviceIncomingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('deviceID', "qrID", "company", "leaseCompany",)

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

    def create_or_update(self,data):

        if Device.objects.filter(deviceID=data["deviceID"]).exists():
            device = Device.objects.get(deviceID=data["deviceID"])
            data["leaseCompany"] = data["leaseCompanyID"]
            serializer = DeviceIncomingSerializer(instance=device, data=data)
            serializer.is_valid(raise_exception=True)
            return serializer.save()
        self.is_valid(raise_exception=True)
        return self.save()

    def update(self, instance, validated_data):
        fields=instance._meta.fields
        exclude=["deviceID"]
        for field in fields:
            field=field.name.split('.')[-1] #to get coulmn name
            if field in exclude:
                continue
            exec("instance.%s = validated_data.get(field, instance.%s)"%(field,field))
        # instance.email = validated_data.get('email', instance.email)
        # instance.name = validated_data.get('name', instance.name)
        # instance.address = validated_data.get('address', instance.address)
        instance.save(consumed = True)
        return instance

    def create(self, validated_data):
        deviceInstance = Device(**validated_data)
        deviceInstance.save(consumed = True)
        return deviceInstance

    def update(self, instance, validated_data):
        fields=instance._meta.fields
        exclude=["id"]
        for field in fields:
            field=field.name.split('.')[-1] #to get coulmn name
            if field in exclude:
                continue
            exec("instance.%s = validated_data.get(field, instance.%s)"%(field,field))
        instance.save(consumed = True)
        return instance
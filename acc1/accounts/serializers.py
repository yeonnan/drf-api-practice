from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    # 이메일 중복 검사
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("존재하는 이메일 입니다.")
        return value

    # 닉네임 중복 검사
    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("존재하는 닉네임 입니다.")
        return value

    # 비밀번호 길이 검증
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 8글자 이상이어야 합니다.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            nickname=validated_data["nickname"],
        )
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'email']


    def validate_email(self, value):
        user = self.instance
        # exclude : 특정 조건에 해당하는 객체를 제외하고 나머지 반환
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("사용중인 이메일 입니다.")
        return value
    

    def validate_nickname(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(nickname=value).exists():
            raise serializers.ValidationError("사용중인 닉네임 입니다.")
        return value
    

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 8글자 이상이어야 합니다.")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
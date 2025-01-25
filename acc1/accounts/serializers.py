from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


        # 이메일 중복 검사
        def validate_email(self, value):
            # value : 유효성 검사에서 사용되는 현재 필드(email)의 값을 의미
            # filter : email 필터가 value와 동일한 레코드를 찾음
            # exists : 쿼리 결과가 존재하는지 반환 (있으면 true, 없으면 false)
            # user 테이블에서 주어진 value와 같은 email이 있는지 확인. 있으면 if 실행, 없으면 if 실행 x
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError('존재하는 이메일 입니다.')
            return value
        
        # 닉네임 중복 검사
        # django orm은 반드시 필드 이름=값 형식으로 저장
        def validate_nickname(self, value):
            if User.objects.filter(nickname=value):
                # validationerror : serializer에서 유효하지 않은 데이터를 사용자에게 알리는 역할
                raise serializers.ValidationError('존재하는 닉네임 입니다.')
            return value
from rest_framework import serializers
from apps.users.models import CustomUser, Role


class AssignRoleSerializer(serializers.Serializer):
    """Oddiy user sifatida ro'yxatdan o'tgan foydalanuvchiga rol berish uchun serializer"""
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(
        choices=[
            (Role.PROJECT_MANAGER, "Project Manager"),
            (Role.DEVELOPER, "Developer"),
            (Role.TESTER, "Tester"),
        ]
    )

    def validate_user_id(self, value):
        try:
            user = CustomUser.objects.get(id=value)
            if not user.is_active:
                raise serializers.ValidationError("Foydalanuvchi faol emas")
            return value
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Foydalanuvchi topilmadi")

    def validate_role(self, value):
        """Faqat ruxsat etilgan rollarni berish mumkin"""
        allowed_roles = [Role.PROJECT_MANAGER, Role.DEVELOPER, Role.TESTER]
        if value not in allowed_roles:
            raise serializers.ValidationError("Noto'g'ri rol tanlandi")
        return value

    def validate(self, attrs):
        """Qo'shimcha validatsiyalar"""
        user_id = attrs['user_id']
        new_role = attrs['role']

        try:
            user = CustomUser.objects.get(id=user_id)

            # Agar user allaqachon project_owner bo'lsa, uning rolini o'zgartirib bo'lmaydi
            if user.role == Role.PROJECT_OWNER:
                raise serializers.ValidationError(
                    "Project Owner ning rolini o'zgartirib bo'lmaydi"
                )

            # Agar user allaqachon shu rolga ega bo'lsa
            if user.role == new_role:
                raise serializers.ValidationError(
                    f"User allaqachon {new_role} roliga ega"
                )

        except CustomUser.DoesNotExist:
            pass

        return attrs


class UserRoleSerializer(serializers.ModelSerializer):
    """Foydalanuvchi va uning roli haqida ma'lumot"""
    full_name = serializers.SerializerMethodField()
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'role', 'role_display', 'is_active']
        read_only_fields = ['id', 'email', 'is_active']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class UserListSerializer(serializers.ModelSerializer):
    """User larni ro'yxatini ko'rsatish uchun"""
    full_name = serializers.SerializerMethodField()
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'role', 'role_display']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

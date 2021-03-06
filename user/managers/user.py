from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, nickname, password, phone_number):
        if not email:
            raise ValueError("유저 생성시 email은 필수입니다.")
        if not password:
            raise ValueError("유저 생성시 password는 필수입니다.")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            nickname=nickname,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, nickname, password, phone_number):
        user = self.create_user(
            email=email,
            name=name,
            nickname=nickname,
            password=password,
            phone_number=phone_number,
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

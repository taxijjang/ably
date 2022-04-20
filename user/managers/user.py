from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, password):
        if not email:
            raise ValueError("유저 생성시 email은 필수입니다.")
        if not password:
            raise ValueError("유저 생성시 password는 필수입니다.")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        if not email:
            raise ValueError("유저 생성시 email은 필수입니다.")
        if not password:
            raise ValueError("유저 생성시 password는 필수입니다.")

        user = self.create_user(
            email=email,
            password=password,
            name=name,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user

import datetime
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.http.response import Http404
from rest_framework import generics
from textSaving import settings
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import *
from django.http import Http404


# Create your views here.


def passwordrule(password):
    alphabets = digits = special = 0
    password_rule = PasswordRule.objects.filter(status=0).first()
    for i in range(len(password)):
        if password[i].isalpha():
            alphabets = alphabets + 1
        elif password[i].isdigit():
            digits = digits + 1
        else:
            special = special + 1
    if password_rule.minimumcharaters > len(
        password
    ) or password_rule.maximumcharaters < len(password):
        return {
            "Status": "1",
            "Message": "Password length must be greater than eight characters or less than fifteen character",
        }
    if special > password_rule.specialcharaters or special == 0:
        return {
            "Status": "1",
            "Message": "The password must contain at least one special character and  at most three special characters",
        }
    if digits < password_rule.uppercase:
        return {
            "Status": "1",
            "Message": "The password must contain at least one digit",
        }


class Changepassword(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, user_id):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user_obj = User.objects.filter(user_id=user_id).first()
            if check_password(data["old_password"], user_obj.password):
                if data["old_password"] == data["new_password"]:
                    return Response(
                        {
                            "status": "1",
                            "message": (
                                "Your password matches with current one. Please enter a new password"
                            ),
                        }
                    )
                response = passwordrule(data["new_password"])
                if response != None:
                    return Response(response)
                if data["new_password"] == data["confirmpassword"]:
                    user_obj.password = make_password(data["new_password"])
                    user_obj.save()
                    return Response(
                        {
                            "status": "0",
                            "message": ("Your password is updated successfully."),
                        }
                    )
                else:
                    return Response(
                        {
                            "status": "0",
                            "message": ("Newpassword and confirm is not matched."),
                        }
                    )
            else:
                return Response(
                    {"status": "0", "message": ("Your old password is not matched.")}
                )
        else:
            return Response({"status": "1", "message": serializer.errors})


class UserRegister(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data
            try:
                response = passwordrule(data["password"])
                if response != None:
                    return Response(response)
                user_object = serializer.save()
                user_obj = User.objects.get(username=data["username"])
                role_obj = Role.objects.get(name="USER")
                datas = {"user_id_id": user_obj.user_id, "role_id_id": role_obj.role_id}
                UserRole.objects.create(**datas)
            except Exception as e:
                # print(str(e))
                return Response(
                    {
                        "Status": "1",
                        "Message": "User creation failed!",
                    }
                )
            return Response(
                {
                    "Status": "0",
                    "Message": "User Successfully created!",
                    "user_id ": user_obj.user_id,
                }
            )
        else:
            return Response(
                {"Status": "1", "Message": serializer.errors},
            )


class UserList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            data_obj = User.objects.filter(status=0)
        except:
            raise Http404
        dataarr = []
        for data_objs in data_obj:
            dict = {
                "user_id": data_objs.user_id,
                "email": data_objs.email,
                "first_name": data_objs.first_name,
                "last_name": data_objs.last_name,
                "mobile_phone": data_objs.mobile_phone,
                "date_joined": data_objs.date_joined,
            }
            dataarr.append(dict)
        if dataarr == []:
            return Response(
                {
                    "Status": "1",
                    "Message": "No User Found",
                }
            )
        return Response(
            {
                "Status": "0",
                "data": dataarr,
            }
        )


class UserById(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self, pk):

        try:

            return User.objects.get(pk=pk, status=0)

        except User.DoesNotExist:

            raise Http404

    def get(self, request, pk, format=None):

        details = self.get_object(pk)

        serializer = UserSerializer(details)

        return Response(serializer.data)

    def put(self, request, pk, format=None):

        details = self.get_object(pk)
        try:
            user_obj = User.objects.get(
                Q(username__iexact=request.data["username"]), ~Q(pk=pk)
            )
            if user_obj:
                return Response(
                    {
                        "Status": "1",
                        "Message": {"username": ["Username already exists."]},
                    }
                )
        except User.DoesNotExist:
            pass
        try:
            if request.data["email"]:
                user_obj = User.objects.get(
                    Q(email__iexact=request.data["email"]), ~Q(pk=pk)
                )
                if user_obj:
                    return Response(
                        {"Status": "1", "Message": {"email": ["Email already exists."]}}
                    )
        except User.DoesNotExist:
            pass
        data = request.data
        serializer = UserSerializer(details, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "Status": "0",
                    "Message": "Successfully Updated!",
                    "Body": serializer.data,
                }
            )

        return Response(
            serializer.errors,
        )

    def delete(self, request, pk, format=None):
        try:
            details = details = self.get_object(pk)
        except:
            return Response({"Status": "1", "Message": "User not found"})
        try:
            details.status = 1
            details.save()
            return Response({"Status": "0", "Message": "User deleted"})
        except:
            return Response({"Status": "1", "Message": "Deletion failed!"})


class Login(APIView):
    serializer = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            try:
                try:
                    user_obj = User.objects.get(
                        Q(username__iexact=data["username"])
                        | Q(email__iexact=data["username"])
                    )
                    if user_obj:
                        if check_password(data["password"], user_obj.password):
                            user_obj.last_login = datetime.datetime.now()
                            user_obj.save()
                            user = User.objects.get(username=user_obj.username)
                            user_role = UserRole.objects.get(
                                user_id_id=user_obj.user_id
                            )
                            refresh_token = RefreshToken.for_user(user)

                            return Response(
                                {
                                    "message": "Successfully logged_in",
                                    "status": 0,
                                    "access_token": str(refresh_token.access_token),
                                    "refresh_token": str(refresh_token),
                                    "user_id": user_obj.user_id,
                                    "first_name": user_obj.first_name,
                                    "last_name": user_obj.last_name,
                                    "mobile_phone": user_obj.mobile_phone,
                                    "username": user_obj.username,
                                    "email": user_obj.email,
                                    "last_login": user_obj.last_login,
                                    "role_name": str(user_role.role_id.name),
                                    "role_id": user_role.role_id_id,
                                }
                            )
                        else:
                            return Response(
                                {"message": "Invalid Password", "status": "1"}
                            )
                except Exception as e:
                    # print(str(e))
                    return Response({"message": "Invalid User", "status": "1"})
                if user_obj.status != 0:
                    return Response({"message": "Inactive User", "status": "1"})
            except Exception as e:
                print("Login Error:", str(e))
        else:
            return Response(
                serializer.errors,
            )

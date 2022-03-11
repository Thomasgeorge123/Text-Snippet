from django.db.models import Q
from django.http.response import Http404
from rest_framework import generics
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import *
from django.http import Http404

# Create your views here.


class Tags(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = TagSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data
            try:
                tag_obj = Tag.objects.get(
                    Q(title__iexact=request.data["title"].title())
                )
                if tag_obj:
                    return Response(
                        {
                            "Status": "1",
                            "Message": {
                                "title": ["tag with this title already exists."]
                            },
                        }
                    )
            except:
                pass
            user_object = serializer.save()
            return Response(
                {
                    "Status": "0",
                    "Message": "Successfully created!",
                }
            )
        else:
            return Response(
                {"Status": "1", "Message": serializer.errors},
            )

    def get(self, request, format=None):
        try:
            data_obj = Tag.objects.filter(status=0)
        except:
            raise Http404
        dataarr = []
        for data_objs in data_obj:
            dict = {
                "tag_id": data_objs.tag_id,
                "title": data_objs.title,
            }
            dataarr.append(dict)
        if dataarr == []:
            return Response(
                {
                    "Status": "1",
                    "Message": "No Data Found",
                }
            )
        return Response(
            {
                "Status": "0",
                "data": dataarr,
            }
        )


class Snippets(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data
            title = request.data["title"].title()
            try:
                tag_obj = Tag.objects.get(Q(title__iexact=title))
                if tag_obj:
                    datas = {
                        "tag_id_id": tag_obj.tag_id,
                        "text": request.data["text"],
                        "user_id_id": request.data["user_id"],
                    }
                    Snippet.objects.create(**datas)
                    return Response(
                        {
                            "Status": "0",
                            "Message": "Successfully created!",
                        }
                    )
            except Exception as e:
                # print(str(e))
                data = {"title": title}
                tag_obj = Tag.objects.create(**data)

                datas = {
                    "tag_id_id": tag_obj.tag_id,
                    "text": request.data["text"],
                    "user_id_id": request.data["user_id"],
                }
                Snippet.objects.create(**datas)

                return Response(
                    {
                        "Status": "0",
                        "Message": "Successfully created!",
                    }
                )
        else:
            return Response(
                {"Status": "1", "Message": serializer.errors},
            )

    def get(self, request, format=None):
        try:
            data_obj = Snippet.objects.filter(status=0)
        except:
            raise Http404
        dataarr = []
        for data_objs in data_obj:
            dict = {
                "snippet_id": data_objs.snippet_id,
                "user_id": data_objs.user_id_id,
                "created_by": data_objs.user_id.username,
                "tag_id": data_objs.tag_id_id,
                "title": data_objs.tag_id.title,
                "snippets": data_objs.text,
                "time_stamp": data_objs.time_stamp,
            }
            dataarr.append(dict)
        if dataarr == []:
            return Response(
                {
                    "Status": "1",
                    "Message": "No Data Found",
                }
            )
        return Response(
            {
                "Status": "0",
                "data": dataarr,
            }
        )


class SnippetById(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SnippetsSerializer

    def get(self, request, pk, format=None):
        try:
            dataarr = []
            details = Snippet.objects.get(pk=pk, status=0)
            dict = {
                "snippet_id": details.snippet_id,
                "user_id": details.user_id_id,
                "created_by": details.user_id.username,
                "title": details.tag_id.title,
                "tag_id": details.tag_id_id,
                "snippets": details.text,
                "time_stamp": details.time_stamp,
            }
            dataarr.append(dict)
            return Response(
                {
                    "Status": "0",
                    "data": dataarr,
                }
            )
        except Snippet.DoesNotExist:

            raise Http404

    def put(self, request, pk, format=None):

        try:
            details = Snippet.objects.get(pk=pk, status=0)
        except Snippet.DoesNotExist:

            raise Http404
        serializer = SnippetsSerializer(details, data=request.data)
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
            details = Snippet.objects.get(pk=pk, status=0)
        except:
            return Response({"Status": "1", "Message": "Not found"})
        try:
            details.status = 1
            details.save()
            dataarr = []
            details_objs = Snippet.objects.get(pk=pk, status=1)
            dict = {
                "snippet_id": details_objs.snippet_id,
                "user_id": details_objs.user_id_id,
                "created_by": details_objs.user_id.username,
                "title": details_objs.tag_id.title,
                "tag_id": details_objs.tag_id_id,
                "snippets": details_objs.text,
                "time_stamp": details_objs.time_stamp,
            }
            dataarr.append(dict)
            return Response(
                {
                    "Status": "0",
                    "Message": "Data deleted",
                    "data": dataarr,
                }
            )
        except Exception as e:
            # print(str(e))
            return Response({"Status": "1", "Message": "Deletion failed!"})


class SnippetByTagId(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, tag_id, format=None):
        try:
            dataarr = []
            detail = Snippet.objects.filter(tag_id_id=tag_id, status=0)
            for details in detail:
                dict = {
                    "snippet_id": details.snippet_id,
                    "user_id": details.user_id_id,
                    "created_by": details.user_id.username,
                    "title": details.tag_id.title,
                    "tag_id": details.tag_id_id,
                    "snippets": details.text,
                    "time_stamp": details.time_stamp,
                }
                dataarr.append(dict)
            return Response(
                {
                    "Status": "0",
                    "data": dataarr,
                }
            )
        except Snippet.DoesNotExist:

            raise Http404


class Overview(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            dataarr = []
            detail = Snippet.objects.filter(status=0)
            for details in detail:
                dict = {
                    "snippet_id": details.snippet_id,
                    "user_id": details.user_id_id,
                    "created_by": details.user_id.username,
                    "title": details.tag_id.title,
                    "tag_id": details.tag_id_id,
                    "snippets": details.text,
                    "time_stamp": details.time_stamp,
                }
                dataarr.append(dict)
            return Response(
                {
                    "Status": "0",
                    "total_count": detail.count(),
                    "data": dataarr,
                }
            )
        except Snippet.DoesNotExist:

            raise Http404

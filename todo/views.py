# # class based views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from todo.models import Todo
from todo.serializers import TodoSerializers
from todo.pagination import PaginationDemo

# #1. Get
class TodoApiView(APIView):
    # @
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("id")
        paginator= PaginationDemo()
        # breakpoint()
        if pk:
            try:
                todos = Todo.objects.get(id=pk)
                serializer = TodoSerializers(todos)
            except:
                return Response({"mess": "not found"}, status=404)

        else:
            """
            List all the todo items for given requested user
            """
            todos = Todo.objects.all()
            result=paginator.paginate_queryset(todos, request)
            serializer = TodoSerializers(result, many=True)
            #return Response(serializer.data, status=status.HTTP_200_OK)
            return paginator.get_paginated_response(serializer.data)


    # 2. Create
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[
                "title",
                "description",
            ],
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def post(self, request, *args, **kwargs):
        """
        Create the Todo with given todo data
        """
        data = {
            "description": request.data.get("description"),
            #'title': request.title.id
            "title": request.data.get("title"),
        }
        serializer = TodoSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Patch
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[
                "title",
                "description",
                "id",
            ],
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "id": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        consumes=["multipart/form-data"],
        responses={201: "Data created", 400: "Bad request"},
    )
    def patch(self, request):
        """
        Update the todo item with given todo_id if exsits
        """
        todo_id = request.data.get("id")
        todo_instance = Todo.objects.get(pk=todo_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        
        serializer = TodoSerializers(todo_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response({"res": "Object updated!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[
                
                "id",
            ],
            properties={
            
                "id": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        consumes=["multipart/form-data"],
        responses={201: "Data deleted", 400: "Bad request"},
    )
    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        todo_ins = Todo.objects.get(id=id)
        if not todo_ins:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        todo_ins.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)


# # # MODELVIEWSET
# from rest_framework import viewsets
# from todo.models import Todo
# from .serializers import TodoSerializers

# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializers
    

#  Functional View set 


# @api_view(['GET','POST']) 
# def todolist(request): 
#     """ 
#     List all transformers, or create a new transformer 
#     """
#     if request.method == 'GET': 
#         transformer = Todo.objects.all() 
#         serializer = TodoSerializers(transformer, many=True) 
#         return Response(serializer.data) 
  
#     elif request.method == 'POST': 
#         serializer =TodoSerializers(data=request.data) 
#         if serializer.is_valid(): 
#             serializer.save() 
#             return Response(serializer.data, 
#                             status=status.HTTP_201_CREATED) 
#         return Response(serializer.errors, 
#                         status=status.HTTP_400_BAD_REQUEST) 
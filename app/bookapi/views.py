from distutils.util import strtobool
from rest_framework import viewsets 

from rest_framework.decorators import api_view, permission_classes #for no model 
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from rest_framework import filters

from .serializers import BookSerializer, AvailableBookSerializer

from .models import Book, AvailableBook, bookapiUserSettings, bookapiSourceFiles

from .extra_methods import BookProcessing

class BookViewSet(viewsets.ModelViewSet): 
	permission_classes = (IsAuthenticated,)
	'''
	model based:
	define queryset
	specify serializer to be used
	set fields to allow automated search queries, 
	note:
	foreign key uses double underscore notation	(double underscore for search into related table)
	'''
	queryset = Book.objects.all()  
	serializer_class = BookSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['title'] 

class AvailableBookViewSet(viewsets.ModelViewSet): 
	permission_classes = (IsAuthenticated,)
	
	queryset = AvailableBook.objects.all()  
	serializer_class = AvailableBookSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'author', 'book'] 

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def settings(request):
	
	if request.method == 'GET':
		obj = bookapiUserSettings.objects.all().values()
		returnData = obj
		return Response(returnData)

	if request.method == 'POST':
		objSettings = bookapiUserSettings.objects.first()
		objSettings.source_ip = request.POST.get('source_ip')
		objSettings.source_script_path = request.POST.get('source_script_path')
		objSettings.save()
		returnData = bookapiUserSettings.objects.all().values()
		return Response(returnData)

	return Response({"message": "settings, GET settings values, POST new settings values"})

@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
def refresh(request):
	
	if request.method == 'PUT':
		obj = BookProcessing()
		returnData = obj.RefreshBooks()
		return Response(returnData)

	return Response({"message": "refresh, PUT perform refresh to update DB"})

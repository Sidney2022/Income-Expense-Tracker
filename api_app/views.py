from django.shortcuts import render
from rest_framework.views import APIView
from income.models import UserIncome
from expense.models import Expense
from rest_framework.views import Response
from django.http import HttpResponse, JsonResponse
from .serializers import UserIncomeSerializer, ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage



class IncomeView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        qs = UserIncome.objects.filter(owner=request.user)
        serializer = UserIncomeSerializer(qs, many=True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        try:
            owner=request.user
            source =request.data['source']
            amount =request.data['amount']
            
            description =request.data['description']
            income_obj = UserIncome.objects.create(owner=owner, source=source, amount=amount, description=description)
            income_obj.save()
            return JsonResponse({"MSG":"Created"})
        except Exception as e:
            return JsonResponse({"Error":f'{e} is required'})
    
    
    def delete(self, request, *args, **kwargs):
        id = request.data['id']
        try:
            income = UserIncome.objects.get(owner=request.user, id=id)
            income.delete()
            return JsonResponse({"Success":"Object deleted successfully"})
        except Exception as e:
            return JsonResponse({"Error":f"could not be completed because {e}"})


def api_docs_home(request):
    return render(request, 'api/index.html')



def api_docs(request):
    return render(request, 'api/docs-page.html')
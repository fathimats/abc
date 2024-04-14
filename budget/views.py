from django.shortcuts import render

from rest_framework.response import Response

from rest_framework import status

from rest_framework.views import APIView

from budget.serializers import UserSerializer,ExpenseSerializer,IncomeSerializer

from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView,DestroyAPIView,UpdateAPIView

from rest_framework.viewsets import ViewSet

from rest_framework import authentication,permissions

from budget.models import Expense,Income

from django.contrib.auth.models import User

from budget.permissions import IsOwner,IsOwnerOrAdmin

from django.utils import timezone 

from django.db.models import Sum


class SignupView(CreateAPIView):
    serializer_class=UserSerializer
    queryset=User.objects.all()

    # def post(self,request,*args,**kwargs):
    #     serializer_instance=UserSerializer(data=request.data)
    #     if serializer_instance.is_valid():
    #         serializer_instance.save()
    #         return Response(data=serializer_instance.data,status=status.HTTP_201_CREATED)
    #     return Response(data=serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)


class ExpenseViewSetView(ViewSet):

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=Expense.objects.filter(owner=request.user)
        serializer_instance=ExpenseSerializer(qs,many=True)
        return Response(data=serializer_instance.data,status=status.HTTP_200_OK)
    

    def create(self,request,*args,**kwargs):
        serializer_instance=ExpenseSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(owner=request.user)
            return Response(data=serializer_instance.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ExpenseDetailView(RetrieveAPIView,DestroyAPIView,UpdateAPIView):

    serializer_class=ExpenseSerializer

    queryset=Expense.objects.all()

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]

# _______________________________income________________________________________

class IncomeListCreateView(ListAPIView,CreateAPIView):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=IncomeSerializer
    queryset=Income.objects.all()

    def get_queryset(self):
        qs=Income.objects.filter(owner=self.request.user)
        return qs
    
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)
        

    # def post(self,request,*args,**kwargs):
    #     serializer_instance=IncomeSerializer(data=request.data)
    #     if serializer_instance.is_valid():
    #         serializer_instance.save(owner=request.user)
    #         return Response(data=serializer_instance.data,status=status.HTTP_201_CREATED)
    #     return Response(data=serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)

    





    # ___________viewset______
    # def list(self,request,*args,**kwargs):
    #     qs=Income.objects.filter(owner=request.user)
    #     serializer_instance=IncomeSerializer(qs,many=True)
    #     return Response(data=serializer_instance.data,status=status.HTTP_200_OK)
    

    # def create(self,request,*args,**kwargs):
    #     serializer_instance=IncomeSerializer(data=request.data)
    #     if serializer_instance.is_valid():
    #         serializer_instance.save(owner=request.user)
    #         return Response(data=serializer_instance.data,status=status.HTTP_201_CREATED)
    #     return Response(data=serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)


class IncomeDetailView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):

    serializer_class=IncomeSerializer

    queryset=Income.objects.all()

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[IsOwner,IsOwnerOrAdmin]

# localhost:8000/api/v1/summary/
# method:get
# data:nill
# authentication

class TransactionSummaryView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args,**kwargs):

        cur_month=timezone.now().month

        cur_year=timezone.now().year

        all_expenses=Expense.objects.filter(owner=request.user,
                                            created_date__year=cur_year,
                                            created_date__month=cur_month)
        
        all_incomes=Income.objects.filter(owner=request.user,
                                            created_date__year=cur_year,
                                            created_date__month=cur_month)
        
        total_expense=all_expenses.values("amount").aggregate(total_expense=Sum("amount"))

        total_income=all_incomes.values("amount").aggregate(total_income=Sum("amount"))

        expense_summary=list(all_expenses.values("category").annotate(total=Sum("amount")))
        
        income_summary=list(all_expenses.values("category").annotate(total=Sum("amount")))


        print("exp total",total_expense)

        print("income total",total_income)

        print("expense summary",expense_summary)

        print("income summary",income_summary)

        data = {}

        total_expense=total_expense.get("total") or 0

        total_income=total_income.get("total") or 0

        data["savings"]=total_income-total_expense



        data["expense_total"] = total_expense

        data["income_total"] = total_income

        data["expense_summary"] = expense_summary

        data["income_summary"] = income_summary

        priority_summary=list(all_expenses.values("priority").annotate(total=Sum("amount")))

        data["expense_priority_summary"]=priority_summary




        return Response(data=data)





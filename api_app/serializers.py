from rest_framework import serializers
from income.models import UserIncome
from expense.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = (
            'id', 'amount', 'category', 'description', 'date'
        )
        
        
class UserIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIncome
        fields = (
            'id', 'amount', 'source', 'description', 'date'
        )
        
        
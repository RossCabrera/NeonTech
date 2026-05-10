from ..forms.auth_forms import LoginForm, RegisterForm
from .admin_forms import OrderStatusForm, ProductForm
from .client_forms import PaymentForm

# Esto permite importar directamente desde core.forms
__all__ = [
    'LoginForm', 
    'RegisterForm',  
    'PaymentForm',
    'ProductForm',
    'OrderStatusForm'
]
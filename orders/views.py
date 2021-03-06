import stripe
from django.contrib.auth.models import Permission
from django.conf import settings
from django.shortcuts import render
from django.views.generic.base  import TemplateView


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

# Create your views here.
class OrdersPageView(TemplateView):
    template_name = "orders/purchase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stripe_test_publishable_key"] = settings.STRIPE_TEST_PUBLISHABLE_KEY
        return context


def charge(request):
    template = 'orders/charge.html'
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=3900,
            currency='usd',
            description='Example charge',
            source = request.POST['stripeToken']
        )
        if charge:
            # get permission
            permission = Permission.objects.get(codename='special_status')

            # get user and add to the user's permission set for payment
            user = request.user
            user.user_permissions.add(permission)
            
    return render(request, template)
    
    

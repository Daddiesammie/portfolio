# views.py
import logging
import uuid
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from pypaystack2 import Paystack
from .models import Payment
from .forms import PaymentForm
from projects.models import Project

logger = logging.getLogger(__name__)
paystack = Paystack(auth_key=settings.PAYSTACK_SECRET_KEY)


@login_required
def initiate_payment(request, project_id):
    """Initialize a payment transaction for a project."""
    project = get_object_or_404(Project, id=project_id)
    
    if project.author == request.user:
        messages.error(request, "You cannot pay for your own project.")
        return redirect('projects:project_detail', project_id=project_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, project=project)
        if form.is_valid():
            try:
                # Create payment record
                payment = form.save(commit=False)
                payment.user = request.user
                payment.project = project
                payment.reference = f"PAY-{uuid.uuid4().hex[:12].upper()}"
                payment.save()

                # Handle AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'reference': payment.reference,
                        'amount_kobo': payment.amount_in_kobo,
                    })

                # Direct Paystack initialization
                response = paystack.transaction.initialize(
                    amount=payment.amount_in_kobo,
                    email=request.user.email,
                    reference=payment.reference,
                    callback_url=request.build_absolute_uri(reverse('payments:verify_payment'))
                )
                
                # Get authorization URL and redirect
                auth_url = response['data']['authorization_url']
                return redirect(auth_url)

            except Exception as e:
                logger.error(f"Payment failed: {str(e)}")
                messages.error(request, "Payment initialization failed. Please try again.")
                return redirect('payments:initiate_payment', project_id=project_id)
    
    # GET request - show payment form
    form = PaymentForm(initial={'amount': getattr(project, 'price', None)}, project=project)
    
    return render(request, 'payments/initiate_payment.html', {
        'form': form,
        'project': project,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
    })

@login_required
def verify_payment(request):
    """Verify a payment transaction."""
    reference = request.GET.get('reference')
    if not reference:
        messages.error(request, "No payment reference provided")
        return redirect('payments:payment_history')  # Updated to use namespace
    
    try:
        payment = get_object_or_404(Payment, reference=reference, user=request.user)
        
        if payment.status == 'success':
            messages.info(request, "Payment was already verified")
            return redirect('payments:payment_success', payment_id=payment.id)
        
        response = paystack.transactions.verify(reference)
        
        if response['data']['status'] == 'success':
            paid_amount = Decimal(response['data']['amount']) / 100
            if paid_amount != payment.amount:
                logger.error(f"Amount mismatch for payment {reference}")
                payment.status = 'failed'
                payment.save()
                messages.error(request, "Payment amount verification failed")
                return redirect('payments:payment_history')
            
            payment.status = 'success'
            payment.save()
            
            messages.success(request, "Payment verified successfully")
            return redirect('payments:payment_success', payment_id=payment.id)
        
        payment.status = 'failed'
        payment.save()
        messages.error(request, "Payment verification failed")
        
    except Exception as e:
        logger.exception(f"Payment verification error: {str(e)}")
        messages.error(request, "An unexpected error occurred during verification")
    
    return redirect('payments:payment_history')


@login_required
def payment_success(request, payment_id):
    """Display payment success page."""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'payments/payment_success.html', {'payment': payment})

@login_required
def payment_history(request):
    """Display user's payment history."""
    # Updated to join with Project and filter by user's payments
    payments = Payment.objects.filter(
        user=request.user
    ).select_related('project').order_by('-created_at')
    return render(request, 'payments/payment_history.html', {'payments': payments})
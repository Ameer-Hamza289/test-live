from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Contact
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create your views here.
@ensure_csrf_cookie
@require_http_methods(["POST"])
def inquiry(request):
    if request.method == 'POST':
        try:
            # Debug: Print all POST data
            print("=== CONTACT FORM SUBMISSION ===")
            print(f"POST data: {dict(request.POST)}")
            print(f"User authenticated: {request.user.is_authenticated}")
            print(f"User ID: {request.user.id if request.user.is_authenticated else 'Anonymous'}")
            print(f"CSRF Cookie: {request.META.get('CSRF_COOKIE', 'Not set')}")
            print(f"Request method: {request.method}")
            print(f"Content type: {request.content_type}")
            print(f"Request path: {request.path}")
            
            # Extract form data with safe defaults
            car_id = request.POST.get('car_id', '0')
            car_title = request.POST.get('car_title', '')
            user_id = request.POST.get('user_id', '0')
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            customer_need = request.POST.get('customer_need', '').strip()
            city = request.POST.get('city', '').strip()
            state = request.POST.get('state', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            message = request.POST.get('message', '').strip()

            print(f"📝 Extracted data:")
            print(f"   - Name: '{first_name}' '{last_name}'")
            print(f"   - Email: '{email}'")
            print(f"   - Phone: '{phone}'")
            print(f"   - City: '{city}', State: '{state}'")
            print(f"   - Car ID: '{car_id}', Title: '{car_title}'")
            print(f"   - User ID: '{user_id}'")
            print(f"   - Customer Need: '{customer_need}'")
            print(f"   - Message: '{message}'")

            # Validate required fields
            required_fields = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                # phone is optional as per frontend template
            }
            
            missing_fields = [field for field, value in required_fields.items() if not value]
            
            if missing_fields:
                error_msg = f"Missing required fields: {', '.join(missing_fields)}"
                print(f"❌ Validation failed: {error_msg}")
                messages.error(request, 'Please fill in all required fields (First Name, Last Name, Email).')
                
                # Redirect back to the form
                if car_id and car_id != '0':
                    return redirect(f'/cars/{car_id}')
                else:
                    return redirect('/contact/')

            print(f"✅ All required fields present")

            # Convert IDs to integers safely
            try:
                car_id_int = int(car_id) if car_id and car_id.isdigit() else 0
                print(f"✅ Car ID converted: {car_id} -> {car_id_int}")
            except (ValueError, TypeError) as e:
                print(f"❌ Car ID conversion failed: {e}")
                car_id_int = 0

            try:
                user_id_int = int(user_id) if user_id and user_id.isdigit() else 0
                print(f"✅ User ID converted: {user_id} -> {user_id_int}")
            except (ValueError, TypeError) as e:
                print(f"❌ User ID conversion failed: {e}")
                user_id_int = 0
                
            # Use authenticated user ID if available
            if request.user.is_authenticated:
                user_id_int = request.user.id
                print(f"✅ Using authenticated user ID: {user_id_int}")

            print(f"🔄 Processing contact: car_id={car_id_int}, user_id={user_id_int}")

            # Create contact record with comprehensive error handling
            try:
                print(f"🔄 Attempting to save contact to database...")
                print(f"🔄 Contact data being saved:")
                print(f"   - car_id: {car_id_int} (type: {type(car_id_int)})")
                print(f"   - car_title: '{car_title}' (type: {type(car_title)})")
                print(f"   - user_id: {user_id_int} (type: {type(user_id_int)})")
                print(f"   - first_name: '{first_name}' (type: {type(first_name)})")
                print(f"   - last_name: '{last_name}' (type: {type(last_name)})")
                print(f"   - customer_need: '{customer_need}' (type: {type(customer_need)})")
                print(f"   - city: '{city}' (type: {type(city)})")
                print(f"   - state: '{state}' (type: {type(state)})")
                print(f"   - email: '{email}' (type: {type(email)})")
                print(f"   - phone: '{phone}' (type: {type(phone)})")
                print(f"   - message: '{message}' (type: {type(message)})")
                
                contact = Contact.objects.create(
                    car_id=car_id_int,
                    car_title=car_title,
                    user_id=user_id_int,
                    first_name=first_name,
                    last_name=last_name,
                    customer_need=customer_need,
                    city=city,
                    state=state,
                    email=email,
                    phone=phone,
                    message=message
                )
                
                print(f"✅ Contact saved successfully with ID: {contact.id}")
                
                # Double-check the save worked by querying the database
                try:
                    saved_contact = Contact.objects.get(id=contact.id)
                    print(f"✅ Verified contact in database: {saved_contact.first_name} {saved_contact.last_name}")
                    print(f"✅ Contact email: {saved_contact.email}")
                    print(f"✅ Contact created: {saved_contact.create_date}")
                    print(f"✅ Contact car_title: {saved_contact.car_title}")
                    print(f"✅ Contact car_id: {saved_contact.car_id}")
                except Contact.DoesNotExist:
                    print(f"❌ CRITICAL: Contact with ID {contact.id} not found after save!")
                    raise Exception("Contact save verification failed")
                
            except Exception as db_error:
                print(f"❌ DATABASE ERROR: {str(db_error)}")
                print(f"❌ Error type: {type(db_error).__name__}")
                
                # Log the data that failed to save
                print(f"❌ Failed data: first_name='{first_name}', last_name='{last_name}', email='{email}'")
                print(f"❌ Failed data: car_id={car_id_int}, user_id={user_id_int}")
                
                import traceback
                traceback.print_exc()
                
                messages.error(request, f'Database error: Unable to save your contact. Please try again. Error: {str(db_error)}')
                
                # Redirect back with error
                if car_id_int > 0:
                    return redirect(f'/cars/{car_id_int}')
                else:
                    return redirect('/contact/')

            messages.success(request, 'Your request has been submitted successfully! We will get back to you shortly.')
            
            # Redirect appropriately
            print(f"✅ Setting success message and redirecting...")
            if car_id_int > 0:
                redirect_url = f'/cars/{car_id_int}'
                print(f"✅ Redirecting to: {redirect_url}")
                return redirect(redirect_url)
            else:
                print(f"✅ Redirecting to: /contact/")
                return redirect('/contact/')

        except Exception as e:
            print(f"❌ CRITICAL ERROR saving contact: {str(e)}")
            print(f"❌ Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            
            messages.error(request, f'There was an error submitting your request. Please try again. Error: {str(e)}')
            
            # Redirect back with error
            referer = request.META.get('HTTP_REFERER', '/contact/')
            return redirect(referer)
    
    # If GET request or other method
    print(f"Non-POST request to inquiry: {request.method}")
    return redirect('/contact/')

# CSRF-exempt version for testing and troubleshooting
@csrf_exempt
@require_http_methods(["POST"])
def inquiry_no_csrf(request):
    """CSRF-exempt version of inquiry for testing purposes"""
    if request.method == 'POST':
        try:
            print("=== CONTACT FORM SUBMISSION (NO CSRF) ===")
            print(f"POST data: {dict(request.POST)}")
            
            # Extract form data
            car_id = request.POST.get('car_id', '0')
            car_title = request.POST.get('car_title', '')
            user_id = request.POST.get('user_id', '0')
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            customer_need = request.POST.get('customer_need', '').strip()
            city = request.POST.get('city', '').strip()
            state = request.POST.get('state', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            message = request.POST.get('message', '').strip()

            # Validate required fields
            if not all([first_name, last_name, email]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Missing required fields: first_name, last_name, email'
                })

            # Convert IDs safely
            try:
                car_id_int = int(car_id) if car_id and car_id.isdigit() else 0
                user_id_int = int(user_id) if user_id and user_id.isdigit() else 0
            except (ValueError, TypeError):
                car_id_int = 0
                user_id_int = 0

            # Create and save contact
            contact = Contact(
                car_id=car_id_int,
                car_title=car_title,
                user_id=user_id_int,
                first_name=first_name,
                last_name=last_name,
                customer_need=customer_need,
                city=city,
                state=state,
                email=email,
                phone=phone,
                message=message
            )

            contact.save()
            print(f"✅ Contact saved (NO CSRF) with ID: {contact.id}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Contact submitted successfully',
                'contact_id': contact.id
            })

        except Exception as e:
            print(f"❌ Error in no-CSRF inquiry: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error', 'message': 'POST required'})

# Test endpoint to verify contact creation works
@csrf_exempt
def test_contact(request):
    """Test endpoint to verify contact functionality"""
    try:
        print("=== TESTING CONTACT CREATION ===")
        
        # Create a test contact
        test_contact = Contact(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            phone='1234567890',
            car_id=1,
            car_title='Test Car',
            user_id=1,
            customer_need='Test inquiry',
            city='Test City',
            state='Test State',
            message='This is a test message'
        )
        
        test_contact.save()
        print(f"✅ Test contact created with ID: {test_contact.id}")
        
        # Verify it exists
        verify_contact = Contact.objects.get(id=test_contact.id)
        print(f"✅ Verified test contact: {verify_contact.first_name} {verify_contact.last_name}")
        
        # Get total count
        total_contacts = Contact.objects.count()
        print(f"📊 Total contacts in database: {total_contacts}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Test contact created successfully',
            'contact_id': test_contact.id,
            'total_contacts': total_contacts
        })
        
    except Exception as e:
        print(f"❌ Test contact creation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

def contact_list_debug(request):
    """Debug endpoint to list all contacts"""
    try:
        contacts = Contact.objects.all().order_by('-create_date')[:10]
        contact_data = []
        
        for contact in contacts:
            contact_data.append({
                'id': contact.id,
                'name': f"{contact.first_name} {contact.last_name}",
                'email': contact.email,
                'phone': contact.phone,
                'car_title': contact.car_title,
                'create_date': contact.create_date.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse({
            'status': 'success',
            'total_contacts': Contact.objects.count(),
            'recent_contacts': contact_data
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

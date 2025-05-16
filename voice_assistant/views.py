from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
import json
import asyncio
from .models import Conversation, CallSession
from django.core.exceptions import ObjectDoesNotExist
from .rag_engine import rag_engine
import os
from dotenv import load_dotenv

load_dotenv()

def voice_assistant(request):
    """Render the voice assistant interface"""
    return render(request, 'voice_assistant/assistant.html')

@csrf_exempt
def test_api(request):
    """Simple test endpoint to verify API functionality"""
    return JsonResponse({
        'status': 'success',
        'message': 'API is working!',
        'method': request.method,
        'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@csrf_exempt
def process_voice(request):
    """Process voice input and return AI response"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id')
            
            if not session_id:
                # Generate a session ID if one isn't provided
                session_id = str(timezone.now().timestamp())
                print(f"No session ID provided, generating one: {session_id}")
            
            # Handle new call start first
            if data.get('is_call_start'):
                # Check if session already exists
                try:
                    session = CallSession.objects.get(session_id=session_id)
                    # If session exists and is not ended, return error
                    if not session.end_time:
                        return JsonResponse({
                            'status': 'success',
                            'response': "I'm still here. What can I help you with?",
                            'is_assistant_response': True
                        })
                    # If session exists but is ended, create a new one
                    session = CallSession.objects.create(
                        session_id=session_id,
                        start_time=timezone.now()
                    )
                except ObjectDoesNotExist:
                    # Create new session if it doesn't exist
                    session = CallSession.objects.create(
                        session_id=session_id,
                        start_time=timezone.now()
                    )
                
                # Initial greeting
                initial_response = "Hello! Thank you for calling our dealership. I'm your AI assistant. How can I help you today?"
                Conversation.objects.create(
                    session=session,
                    speaker='assistant',
                    message=initial_response
                )
                return JsonResponse({
                    'status': 'success',
                    'response': initial_response,
                    'is_assistant_response': True
                })
            
            # For all other operations, verify session exists
            try:
                session = CallSession.objects.get(session_id=session_id)
            except ObjectDoesNotExist:
                # Create a new session on the fly if handling a message but session doesn't exist
                if not data.get('is_call_end'):
                    session = CallSession.objects.create(
                        session_id=session_id,
                        start_time=timezone.now()
                    )
                    print(f"Created new session on the fly: {session_id}")
                else:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'No active session found'
                    })
            
            # Handle call end
            if data.get('is_call_end'):
                if not session.end_time:
                    session.end_time = timezone.now()
                    session.duration = session.end_time - session.start_time
                    session.save()
                
                # Get transcript
                messages = session.messages.all()
                transcript = [{
                    'timestamp': msg.timestamp.strftime('%I:%M:%S %p'),
                    'speaker': msg.speaker.title(),
                    'text': msg.message
                } for msg in messages]
                
                return JsonResponse({
                    'status': 'success',
                    'is_transcript': True,
                    'transcript': transcript
                })
            
            # Regular message processing
            if session.end_time:
                # Reopen session if it was ended
                session.end_time = None
                session.save()
                print(f"Reopened session: {session_id}")
            
            user_input = data.get('text', '')
            if not user_input:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No message provided'
                }, status=400)
            
            # Save user message
            Conversation.objects.create(
                session=session,
                speaker='user',
                message=user_input
            )
            
            # Get conversation history for context
            recent_messages = session.messages.order_by('-timestamp')[:5][::-1]
            conversation_history = [{
                'speaker': msg.speaker,
                'message': msg.message
            } for msg in recent_messages]
            
            try:
                # Get AI response using RAG-enhanced Gemini
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                ai_response = loop.run_until_complete(
                    rag_engine.get_response(user_input, conversation_history)
                )
                loop.close()
                
                # Save AI response
                Conversation.objects.create(
                    session=session,
                    speaker='assistant',
                    message=ai_response
                )
                
                return JsonResponse({
                    'status': 'success',
                    'response': ai_response,
                    'is_assistant_response': True
                })
            except Exception as e:
                print(f"Error getting AI response: {str(e)}")
                error_message = "I apologize, but I'm having trouble processing your request at the moment. Please try again."
                Conversation.objects.create(
                    session=session,
                    speaker='assistant',
                    message=error_message
                )
                return JsonResponse({
                    'status': 'success',
                    'response': error_message,
                    'is_assistant_response': True
                })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

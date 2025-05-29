import os
from typing import List, Dict
import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from dotenv import load_dotenv
import json
import google.generativeai as genai
import django
from django.conf import settings

# Configure Django settings if not already configured
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cardealer.settings')
    django.setup()

from cars.models import Car
from django.db import models

load_dotenv()

# Initialize Google Gemini API settings
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize sentence transformer for embeddings
encoder = SentenceTransformer('all-MiniLM-L6-v2')

class RAGEngine:
    def __init__(self):
        # Base knowledge base with dealership information (non-car specific)
        self.base_knowledge = [
            # Financing Options
            "We offer competitive financing rates starting from 2.9% APR for qualified buyers.",
            "Special financing programs available for first-time buyers and college graduates with rates from 3.9% APR.",
            "Flexible lease terms available from 24 to 60 months with multiple mileage options.",
            "We work with multiple lenders to ensure you get the best possible financing terms.",
            "Zero down payment options available for qualified buyers with excellent credit.",
            "Quick and easy online pre-approval process available through our secure website.",
            
            # Service Department
            "Our service department is staffed with factory-trained technicians certified by major manufacturers.",
            "We offer comprehensive maintenance services including oil changes, tire rotations, brake service, and major repairs.",
            "Express service available for routine maintenance with no appointment necessary.",
            "Complimentary multi-point inspection with every service visit.",
            "Service hours: Monday-Friday 7 AM to 7 PM, Saturday 8 AM to 5 PM.",
            "We use genuine OEM parts for all repairs and maintenance.",
            
            # Special Programs
            "Military personnel receive an additional $500 off their purchase.",
            "College graduate program offers $750 rebate on new vehicle purchases.",
            "First-time buyer program includes reduced down payment requirements and special rates.",
            "Trade-in program offers competitive market value plus an additional $500 towards your new vehicle.",
            
            # Dealership Amenities
            "Comfortable waiting area with complimentary Wi-Fi, coffee, and refreshments.",
            "Courtesy shuttle service available within a 10-mile radius.",
            "Kids play area in the showroom to make your visit more comfortable.",
            "Complimentary car wash with every service visit.",
            
            # Business Hours & Location
            "Sales department hours: Monday-Saturday 9 AM to 7 PM, Sunday 11 AM to 5 PM.",
            "Service center hours: Monday-Friday 7 AM to 7 PM, Saturday 8 AM to 5 PM.",
            "Conveniently located at the intersection of Main Street and Commerce Boulevard.",
            "Easy access from both I-95 and Route 1.",
            
            # Test Drive Policy
            "Test drives available 7 days a week with prior appointment.",
            "Extended test drives up to 24 hours available for serious buyers.",
            "Virtual test drive consultations available through video call.",
            "Multiple vehicles can be test-driven in a single visit.",
            
            # Warranty Information
            "New vehicles come with comprehensive manufacturer warranty coverage.",
            "Extended warranty options available for both new and used vehicles.",
            "Certified pre-owned vehicles include additional 1-year/12,000-mile warranty.",
            "Powertrain warranty coverage up to 10 years/100,000 miles available.",
            
            # Additional Services
            "All our used vehicles undergo a comprehensive 150-point inspection and come with a detailed vehicle history report.",
            "We offer certified pre-owned vehicles from major manufacturers with extended warranty coverage.",
            "Every used vehicle comes with a 7-day/500-mile money-back guarantee.",
            "Free vehicle history reports for all used cars.",
            "Complimentary vehicle appraisals for trade-ins.",
            "Online inventory search with detailed vehicle specifications and photos.",
            "Custom vehicle ordering available for specific model configurations.",
            "Assistance with vehicle registration and insurance.",
        ]
        
        # Session-based caching for car inventory
        self.session_cache = {}
        self.current_session_id = None
        self.knowledge_base = None
        self.embeddings = None
        self.index = None
        
        # Initialize with base knowledge only (no car data yet)
        self.initialize_base_index()

    def initialize_base_index(self):
        """Initialize FAISS index with base knowledge only (no car inventory yet)."""
        self.knowledge_base = self.base_knowledge.copy()
        self.embeddings = encoder.encode(self.knowledge_base)
        self.dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(self.embeddings.astype('float32'))

    def get_or_create_session_context(self, session_id=None):
        """Get cached car inventory context for session, or create if not exists."""
        # If no session provided, use global context (refresh each time)
        if not session_id:
            return self.get_car_inventory_context()
        
        # Check if we have cached context for this session
        if session_id in self.session_cache:
            print(f"Using cached car inventory for session: {session_id}")
            return self.session_cache[session_id]
        
        # Create new context for this session
        print(f"Creating new car inventory context for session: {session_id}")
        car_context = self.get_car_inventory_context()
        self.session_cache[session_id] = car_context
        
        # Clean up old sessions (keep only last 10 sessions to prevent memory bloat)
        if len(self.session_cache) > 10:
            oldest_session = next(iter(self.session_cache))
            del self.session_cache[oldest_session]
            print(f"Cleaned up old session cache: {oldest_session}")
        
        return car_context

    def update_knowledge_base_for_session(self, session_id=None):
        """Update the knowledge base with car inventory for specific session."""
        # Get car inventory (cached for session or fresh)
        car_inventory = self.get_or_create_session_context(session_id)
        
        # Only rebuild if session changed or if we don't have current knowledge base
        if (self.current_session_id != session_id or 
            self.knowledge_base is None or 
            len(self.knowledge_base) == len(self.base_knowledge)):  # No car data yet
            
            print(f"Rebuilding knowledge base for session: {session_id}")
            
            # Combine base knowledge with current inventory
            self.knowledge_base = self.base_knowledge + car_inventory
            
            # Recreate FAISS index with updated knowledge
            self.embeddings = encoder.encode(self.knowledge_base)
            self.dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(self.embeddings.astype('float32'))
            
            # Update current session tracking
            self.current_session_id = session_id
        else:
            print(f"Using existing knowledge base for session: {session_id}")

    def refresh_session_inventory(self, session_id):
        """Force refresh car inventory for a specific session (use when inventory changes)."""
        if session_id in self.session_cache:
            del self.session_cache[session_id]
            print(f"Refreshed inventory cache for session: {session_id}")
        # Next call to get_or_create_session_context will fetch fresh data

    def clear_session_cache(self, session_id=None):
        """Clear cache for specific session or all sessions."""
        if session_id:
            if session_id in self.session_cache:
                del self.session_cache[session_id]
                print(f"Cleared cache for session: {session_id}")
        else:
            self.session_cache.clear()
            self.current_session_id = None
            print("Cleared all session caches")

    def get_car_inventory_context(self):
        """Fetch current car inventory from database and convert to context strings."""
        try:
            cars = Car.objects.all()
            car_contexts = []
            
            # Group cars by model for better organization
            car_models = {}
            for car in cars:
                model_key = f"{car.model} {car.year}".strip()
                if model_key not in car_models:
                    car_models[model_key] = []
                car_models[model_key].append(car)
            
            # Create context for inventory overview
            if cars.exists():
                total_cars = cars.count()
                featured_cars = cars.filter(is_featured=True).count()
                models_available = set(car.model for car in cars)
                years_range = f"{cars.aggregate(min_year=models.Min('year'), max_year=models.Max('year'))['min_year']}-{cars.aggregate(min_year=models.Min('year'), max_year=models.Max('year'))['max_year']}"
                
                car_contexts.append(f"We currently have {total_cars} vehicles in our inventory, with {featured_cars} featured vehicles.")
                car_contexts.append(f"Available models include: {', '.join(sorted(models_available))}.")
                car_contexts.append(f"Our inventory spans model years from {years_range}.")
            
            # Create detailed context for each car
            for car in cars[:20]:  # Limit to first 20 cars to avoid too much context
                # Handle MultiSelectField features properly
                if hasattr(car.features, '__iter__') and not isinstance(car.features, str):
                    # If it's iterable (list-like), join it
                    features_text = ', '.join(car.features) if car.features else 'standard features'
                elif isinstance(car.features, str):
                    # If it's a string, split it
                    features_list = car.features.split(',') if car.features else []
                    features_text = ', '.join(features_list) if features_list else 'standard features'
                else:
                    features_text = 'standard features'
                
                car_context = f"{car.car_title}: {car.year} {car.model} in {car.color}, priced at ${car.price:,}. "
                car_context += f"This {car.condition} vehicle has {car.miles:,} miles, {car.engine} engine, {car.transmission} transmission, "
                car_context += f"{car.doors} doors, seats {car.passengers} passengers, and features {features_text}. "
                car_context += f"Fuel type: {car.fuel_type}, Located in {car.city}, {car.state}."
                
                if car.is_featured:
                    car_context += " This is a FEATURED vehicle with special pricing."
                
                car_contexts.append(car_context)
            
            # Add summary information about different categories
            if cars.exists():
                # Price ranges
                price_ranges = {
                    'under_20k': cars.filter(price__lt=20000).count(),
                    '20k_to_30k': cars.filter(price__gte=20000, price__lt=30000).count(),
                    '30k_to_50k': cars.filter(price__gte=30000, price__lt=50000).count(),
                    'over_50k': cars.filter(price__gte=50000).count(),
                }
                
                price_context = "Price ranges in our inventory: "
                if price_ranges['under_20k'] > 0:
                    price_context += f"{price_ranges['under_20k']} vehicles under $20,000, "
                if price_ranges['20k_to_30k'] > 0:
                    price_context += f"{price_ranges['20k_to_30k']} vehicles $20,000-$30,000, "
                if price_ranges['30k_to_50k'] > 0:
                    price_context += f"{price_ranges['30k_to_50k']} vehicles $30,000-$50,000, "
                if price_ranges['over_50k'] > 0:
                    price_context += f"{price_ranges['over_50k']} vehicles over $50,000."
                
                car_contexts.append(price_context.rstrip(', ') + ".")
            
            return car_contexts
            
        except Exception as e:
            print(f"Error fetching car inventory: {str(e)}")
            return ["We have a variety of quality vehicles available. Please visit our showroom or contact us for current inventory."]

    def get_relevant_context(self, query: str, session_id: str = None, k: int = 5) -> str:
        """Retrieve relevant context from knowledge base using similarity search."""
        # Update knowledge base for this specific session (uses cache if available)
        self.update_knowledge_base_for_session(session_id)
        
        query_vector = encoder.encode([query])[0].reshape(1, -1).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        
        relevant_docs = [self.knowledge_base[i] for i in indices[0]]
        return "\n".join(relevant_docs)

    async def get_response(self, query: str, conversation_history: List[Dict] = None, session_id: str = None) -> str:
        """Generate response using Google Gemini with RAG-enhanced context."""
        try:
            # Get relevant context from knowledge base (with session-based caching)
            context = self.get_relevant_context(query, session_id)
            
            # Prepare conversation history
            history_text = ""
            if conversation_history:
                history_items = []
                for msg in conversation_history[-3:]:  # Last 3 messages for brevity
                    speaker = "Customer" if msg['speaker'] == 'user' else "Assistant"
                    history_items.append(f"{speaker}: {msg['message']}")
                history_text = "\n".join(history_items)
            
            # Create the system prompt
            system_prompt = """You are a car dealership AI assistant named CarBot. Be helpful, friendly, and concise.
You have access to information about our dealership's inventory, services, financing options, and more.
Keep your responses professional but conversational, direct, and to the point - like a helpful dealership employee.
EXTREMELY IMPORTANT:
1. Answer the customer's query ONLY - do not invent additional dialogue or future conversation
2. Do not add hypothetical "Customer:" messages or responses in your answer
3. Do not add any text after your answer
4. Do not provide sample conversations
5. Respond directly to the current query only, as if you were speaking to the customer right now"""

            # Format the entire prompt
            prompt = f"{system_prompt}\n\n"
            prompt += f"Relevant dealership information:\n{context}\n\n"
            
            if history_text:
                prompt += f"Previous conversation:\n{history_text}\n\n"
            
            prompt += f"Customer: {query}\n\nAssistant:"

            # Generate response using Gemini
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.9,
                    top_k=40,
                    max_output_tokens=150,  # Reduced for faster responses
                    candidate_count=1
                )
            )

            if response.text:
                text = response.text.strip()
                
                # Clean up common formatting issues in model responses
                prefixes_to_remove = [
                    "Here's a potential response:", 
                    "Assistant:", 
                    "As the assistant, I would respond:", 
                    "I would respond with:"
                ]
                
                for prefix in prefixes_to_remove:
                    if text.startswith(prefix):
                        text = text[len(prefix):].strip()
                
                # Remove quotes if the entire response is wrapped in them
                if text.startswith('"') and text.endswith('"'):
                    text = text[1:-1].strip()
                    
                # Remove meta-commentary or explanations about the response
                if "This response:" in text:
                    text = text.split("This response:")[0].strip()
                
                # Remove any fabricated customer queries that the model might have hallucinated
                if "Customer:" in text:
                    text = text.split("Customer:")[0].strip()
                
                # Also check for common dialogue indicators
                dialogue_markers = ["Customer:", "User:", "Human:", "Person:"]
                for marker in dialogue_markers:
                    if marker in text:
                        text = text.split(marker)[0].strip()
                
                # Use first-person language
                text = text.replace("the dealership", "our dealership")
                
                return text
            else:
                return "I'm sorry, I'm having trouble accessing our information right now. Can I help you with something else?"

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I'm having trouble with our system right now. Can I take your number and have someone call you back?"

# Initialize RAG engine as a singleton
rag_engine = RAGEngine() 
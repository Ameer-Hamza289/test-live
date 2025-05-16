import os
from typing import List, Dict
import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from dotenv import load_dotenv
import json
import google.generativeai as genai

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
        # Initialize knowledge base with detailed car dealership information
        self.knowledge_base = [
            # Vehicle Inventory
            "Our new vehicle inventory includes latest models from Toyota, Honda, Ford, and Chevrolet, featuring sedans, SUVs, trucks, and hybrid vehicles.",
            "Popular sedan models include Toyota Camry, Honda Accord, and Ford Fusion, starting from $25,000.",
            "Our SUV lineup features Toyota RAV4, Honda CR-V, Ford Explorer, and Chevrolet Tahoe, with prices ranging from $28,000 to $55,000.",
            "We stock a variety of trucks including Ford F-150, Chevrolet Silverado, and Toyota Tundra, perfect for both work and personal use.",
            "Our hybrid and electric vehicle selection includes Toyota Prius, Honda Insight, and Ford Mustang Mach-E.",
            
            # Used Cars
            "All our used vehicles undergo a comprehensive 150-point inspection and come with a detailed vehicle history report.",
            "We offer certified pre-owned vehicles from major manufacturers with extended warranty coverage.",
            "Our used car inventory is priced competitively, with options starting under $15,000.",
            "Every used vehicle comes with a 7-day/500-mile money-back guarantee.",
            "We regularly update our used car inventory with quality vehicles under 5 years old and less than 60,000 miles.",
            
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
            "Free vehicle history reports for all used cars.",
            "Complimentary vehicle appraisals for trade-ins.",
            "Online inventory search with detailed vehicle specifications and photos.",
            "Custom vehicle ordering available for specific model configurations.",
            "Assistance with vehicle registration and insurance.",
        ]
        
        # Create FAISS index for fast similarity search
        self.embeddings = encoder.encode(self.knowledge_base)
        self.dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(self.embeddings.astype('float32'))

    def get_relevant_context(self, query: str, k: int = 5) -> str:
        """Retrieve relevant context from knowledge base using similarity search."""
        query_vector = encoder.encode([query])[0].reshape(1, -1).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        
        relevant_docs = [self.knowledge_base[i] for i in indices[0]]
        return "\n".join(relevant_docs)

    async def get_response(self, query: str, conversation_history: List[Dict] = None) -> str:
        """Generate response using Google Gemini with RAG-enhanced context."""
        try:
            # Get relevant context from knowledge base
            context = self.get_relevant_context(query)
            
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
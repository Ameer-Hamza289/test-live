import os
from typing import List, Dict
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

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
        """Generate response using Gemini with RAG-enhanced context."""
        try:
            # Get relevant context from knowledge base
            context = self.get_relevant_context(query)
            
            # Prepare conversation history
            history_text = ""
            if conversation_history:
                history_text = "\n".join([
                    f"{'Customer' if msg['speaker'] == 'user' else 'Assistant'}: {msg['message']}"
                    for msg in conversation_history[-3:]  # Include last 3 messages for context
                ])

            # Create enhanced prompt with context and history
            history_section = f"Previous conversation:\n{history_text}\n" if history_text else ""
            
            prompt = f"""You are an AI assistant for a car dealership. Be professional, helpful, and concise.
Your role is to assist customers with inquiries about vehicles, services, and dealership information.
Always maintain a friendly and professional tone, and provide specific details from the dealership information when available.

Relevant dealership information:
{context}

{history_section}
Customer: {query}

Please provide a natural, conversational response that:
1. Directly addresses the customer's query
2. Uses specific details from the dealership information
3. Maintains a helpful and professional tone
4. Keeps the response concise but informative
5. Offers relevant follow-up information when appropriate"""

            # Generate response using Gemini
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I apologize, but I'm having trouble processing your request at the moment. Please try again."

# Initialize RAG engine as a singleton
rag_engine = RAGEngine() 
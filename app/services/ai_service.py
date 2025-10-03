import httpx
import os
from dotenv import load_dotenv
import random

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
    
    def generate_question(self, level: int) -> dict:
        """Generate questions locally - INSTANT, no AI latency"""
        
        if level == 1:
            # Level 1: Simple addition (1-10)
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            return {"problem": f"{a} + {b}", "answer": str(a + b)}
            
        elif level == 2:
            # Level 2: Add/subtract (10-20)
            a = random.randint(10, 20)
            b = random.randint(1, 10)
            
            if random.random() > 0.5:
                return {"problem": f"{a} + {b}", "answer": str(a + b)}
            else:
                return {"problem": f"{a} - {b}", "answer": str(a - b)}
                    
        else:  # Level 3
            # Level 3: Multiply/divide (up to 50)
            ops = ['x', '/']
            op = random.choice(ops)
            
            if op == 'x':
                a = random.randint(2, 10)
                b = random.randint(2, 10)
                return {"problem": f"{a} x {b}", "answer": str(a * b)}
            else:
                b = random.randint(2, 10)
                a = b * random.randint(2, 10)
                return {"problem": f"{a} / {b}", "answer": str(a // b)}
    
    async def generate_response(self, is_correct: bool, problem: str, child_age: int = None) -> str:
        """AI generates EXACTLY 2 words"""
        
        if not self.api_key or self.api_key == "your-openai-api-key-here":
            return "Great job!" if is_correct else "Try again!"
        
        # Optional: Adjust language based on child's age
        age_context = ""
        if child_age:
            if child_age < 6:
                age_context = " Use very simple, encouraging language suitable for a young child."
            elif child_age < 9:
                age_context = " Use language appropriate for an elementary school child."
            else:
                age_context = " Use language appropriate for an older elementary school child."
        
        if is_correct:
            prompt = f"""Generate EXACTLY 2 words of encouragement for a child who answered correctly.{age_context}

Examples: "Well done!", "Great job!", "Nice work!", "You rock!", "Amazing work!"

Reply with ONLY 2 words:"""
        else:
            prompt = f"""Generate EXACTLY 2 words of encouragement for a child who answered incorrectly.{age_context}

Examples: "Try again!", "Keep trying!", "Almost there!", "Next time!", "Good attempt!"

Reply with ONLY 2 words:"""
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 10,
                        "temperature": 0.9
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    text = result["choices"][0]["message"]["content"].strip()
                    words = text.split()[:2]
                    return " ".join(words)
                        
        except Exception as e:
            print(f"Error: {e}")
        
        return "Great job!" if is_correct else "Try again!"

ai_service = AIService()
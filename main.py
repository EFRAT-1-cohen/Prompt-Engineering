
import gradio as gr
from openai import OpenAI
import os
from dotenv import load_dotenv
from prompts import EXAMPLE_INPUTS, SYSTEM_PROMPT


load_dotenv()
print("\n" + "="*50)
print("🔍 בודק הגדרות API Key:")
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    print(f"✅ Key נמצא!")
    print(f"   מתחיל ב: {api_key[:20]}...")
    print(f"   מסתיים ב: ...{api_key[-10:]}")
    print(f"   אורך: {len(api_key)} תווים")
else:
    print("❌ OPENAI_API_KEY לא נמצא בסביבה!")
    print(f"   תיקייה נוכחית: {os.getcwd()}")
    print(f"   קובץ .env קיים? {os.path.exists('.env')}")
print("="*50 + "\n")



def translate_to_command(user_input):
    """
    הפונקציה הראשית שעושה את התרגום.
    
    Args:
        user_input (str): הוראה בשפה טבעית מהמשתמש
    
    Returns:
        str: פקודת ה-CLI שנוצרה על ידי המודל
    """
    
   
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        return "❌ שגיאה: OPENAI_API_KEY לא מוגדר. בדקי את קובץ ה-.env"
    
    try:
  
        client = OpenAI(api_key=api_key)
        
   
        response = client.chat.completions.create(
            model="gpt-4o",  
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user", 
                    "content": user_input
                }
            ],
            temperature=0,  
            max_tokens=100  
        )
        
     
        command = response.choices[0].message.content.strip()
        
        return command
    
    except Exception as e:
        return f"❌ שגיאה: {str(e)}"



demo = gr.Interface(
    fn=translate_to_command,
    inputs=gr.Textbox(
        label="הוראה בשפה טבעית",
        placeholder="לדוגמה: מה כתובת ה-IP של המחשב שלי?",
        lines=3,
        rtl=True  
    ),
    outputs=gr.Textbox(
        label="פקודת CLI",
        lines=2,
        rtl=False
    ),
    title="🖥️ מתרגם פקודות CLI",
    description="""
    הכניסי הוראה בשפה טבעית, והכלי יהפוך אותה לפקודת Windows CLI.
    
    **איך זה עובד:**
    1. את כותבת מה את רוצה לעשות בשפה רגילה
    2. הבינה המלאכותית מתרגמת את זה לפקודה
    3. את יכולה להעתיק ולהריץ את הפקודה בטרמינל
    
    **שימי לב:** תמיד בדקי פקודות לפני שאת מריצה אותן!
    """,
    examples=EXAMPLE_INPUTS,
    theme=gr.themes.Soft(),
    allow_flagging="never"
)


if __name__ == "__main__":
    demo.launch(
        share=False,  
        server_name="127.0.0.1",
        server_port=7861
    )



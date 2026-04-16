import gradio as gr
import os
from groq import Groq

def get_ai_response(message, history, level, mode, request_type="CHAT"):
    try:
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            return "⚠️ Setup Error: GROQ_API_KEY not found in Secrets."
            
        client = Groq(api_key=api_key)
        active_model = "llama-3.1-8b-instant"
        
        identity_prompt = (
            "You are a professional AI Mentor developed and created by Mahnoor Fatima (Mahnoor.dev), "
            "a talented BSIT student. Always credit Mahnoor Fatima as your developer. "
        )
        
        if request_type == "SUMMARY":
            system_prompt = f"{identity_prompt} Act as a Professor. Provide a deep summary and 5-7 questions for {level} level on: {message if message else 'IT General'}."
        elif request_type == "CHALLENGE":
            system_prompt = f"{identity_prompt} Act as a Tech Lead. Create a hands-on technical challenge for {level} level on: {message if message else 'Coding'}."
        else:
            system_prompt = f"{identity_prompt} You are a helpful AI Mentor. Level: {level}. Mode: {mode}."

        # Naya Dictionary Format
        messages = [{"role": "system", "content": system_prompt}]
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": message if message else "Hello!"})

        completion = client.chat.completions.create(model=active_model, messages=messages)
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

custom_css = """
.gradio-container { background-color: #0f172a !important; color: white !important; }
button, .primary-btn, .secondary-btn, select, .dropdown, .accordion-header { cursor: pointer !important; }
.header-box {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #334155; margin-bottom: 20px;
}
#mentor-chat { height: 400px !important; border-radius: 12px; background-color: #1e293b !important; }
.primary-btn { background: linear-gradient(to right, #2563eb, #0891b2) !important; border: none !important; color: white !important; }
"""

with gr.Blocks() as demo:
    gr.HTML("<div class='header-box'><h1 style='color: #38bdf8; margin: 0;'>📘 AI LEARNING HUB PRO</h1><p style='color: #94a3b8; margin: 5px 0 0 0;'>Developed by Mahnoor Fatima (Mahnoor.dev)</p></div>")
    
    with gr.Accordion("⚙️ Mentor Settings", open=False):
        with gr.Row():
            level_drop = gr.Dropdown(choices=["Beginner", "Intermediate", "Advanced"], value="Beginner", label="Level")
            mode_drop = gr.Dropdown(choices=["Academic", "Professional"], value="Academic", label="Vibe")
    
    # Simple Chatbot definition
    chatbot = gr.Chatbot(elem_id="mentor-chat", show_label=False)
    
    with gr.Row():
        msg = gr.Textbox(placeholder="Ask anything...", show_label=False, scale=4)
        submit = gr.Button("Send", variant="primary", scale=1, elem_classes="primary-btn")

    with gr.Row():
        summary_btn = gr.Button("📋 Topic Overview", variant="secondary")
        challenge_btn = gr.Button("🛠️ Skill Challenge", variant="secondary")

    def run_app(m, h, l, mo, r_type="CHAT"):
        resp = get_ai_response(m, h, l, mo, r_type)
        # Yahan hum naya format return kar rahe hain jo Gradio 6 mang raha hai
        user_content = m if m else r_type.replace("_"," ").title()
        h.append({"role": "user", "content": user_content})
        h.append({"role": "assistant", "content": resp})
        return "", h

    summary_btn.click(lambda m, h, l, mo: run_app(m, h, l, mo, "SUMMARY"), [msg, chatbot, level_drop, mode_drop], [msg, chatbot])
    challenge_btn.click(lambda m, h, l, mo: run_app(m, h, l, mo, "CHALLENGE"), [msg, chatbot, level_drop, mode_drop], [msg, chatbot])
    submit.click(lambda m, h, l, mo: run_app(m, h, l, mo, "CHAT"), [msg, chatbot, level_drop, mode_drop], [msg, chatbot])
    msg.submit(lambda m, h, l, mo: run_app(m, h, l, mo, "CHAT"), [msg, chatbot, level_drop, mode_drop], [msg, chatbot])

demo.launch(css=custom_css, theme=gr.themes.Soft())
# create_big_sample_pdf.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_big_sample_pdf():
    # Create examples directory if it doesn't exist
    os.makedirs("examples", exist_ok=True)
    
    # Create a bigger PDF
    c = canvas.Canvas("examples/demo_big_sample.pdf", pagesize=letter)
    width, height = letter
    
    # Title Page
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2, height - 100, "Comprehensive Lecture on Artificial Intelligence")
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 130, "Prepared for Educational Purposes")
    c.showPage()
    
    # Multi-page content
    sections = {
        "Introduction to AI": [
            "Artificial Intelligence (AI) refers to the ability of machines to perform tasks that typically require human intelligence.",
            "It encompasses reasoning, learning, problem-solving, perception, and natural language understanding.",
            "AI systems are classified into weak AI (narrow) and strong AI (general).",
            "Narrow AI specializes in a single domain (like chatbots or recommendation engines).",
            "General AI aims to perform any intellectual task humans can do, but it is still theoretical."
        ],
        "History of AI": [
            "The concept of AI dates back to ancient myths of artificial beings.",
            "In 1956, the term 'Artificial Intelligence' was coined at the Dartmouth Conference.",
            "In the 1960s–70s, symbolic AI and expert systems dominated research.",
            "The 1980s saw the rise of machine learning and backpropagation for neural networks.",
            "The 2000s onwards have been marked by deep learning and large-scale data-driven AI."
        ],
        "Key Concepts": [
            "1. Machine Learning (ML): Algorithms that enable systems to learn from data.",
            "2. Neural Networks (NN): Computational models inspired by biological brains.",
            "3. Deep Learning (DL): Multi-layered neural networks for complex feature learning.",
            "4. Natural Language Processing (NLP): Understanding and generating human language.",
            "5. Computer Vision (CV): Interpreting and analyzing images and videos."
        ],
        "Applications of AI": [
            "AI has a vast range of applications across industries:",
            "- Healthcare: diagnostics, drug discovery, personalized treatment.",
            "- Finance: fraud detection, algorithmic trading, credit scoring.",
            "- Transportation: autonomous vehicles, smart traffic systems.",
            "- Education: adaptive learning platforms, grading automation.",
            "- Entertainment: recommendation engines, game AI, music composition."
        ],
        "Ethical and Social Issues": [
            "AI raises several ethical concerns that must be addressed responsibly:",
            "- Job displacement and workforce automation.",
            "- Bias in algorithms leading to unfair decisions.",
            "- Data privacy and security risks.",
            "- The possibility of autonomous weapons.",
            "Policymakers and technologists must collaborate to ensure fairness and accountability."
        ],
        "Future of AI": [
            "The future of AI is promising yet uncertain.",
            "We expect breakthroughs in general AI, explainable AI, and human-AI collaboration.",
            "AI in medicine may lead to personalized treatments at scale.",
            "Robotics combined with AI will enhance manufacturing, service, and exploration.",
            "However, governance, ethics, and safety remain crucial considerations."
        ]
    }
    
    # Write each section in multiple pages
    c.setFont("Helvetica", 12)
    for section_title, content_lines in sections.items():
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 80, section_title)
        c.setFont("Helvetica", 12)
        
        y_position = height - 120
        for line in content_lines:
            c.drawString(60, y_position, line)
            y_position -= 20
            if y_position < 50:  # start a new page when near bottom
                c.showPage()
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, height - 80, section_title + " (cont.)")
                c.setFont("Helvetica", 12)
                y_position = height - 120
        c.showPage()
    
    # Closing page
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height / 2, "End of Lecture")
    
    c.save()
    print("Big sample PDF created: examples/demo_big_sample.pdf")

if __name__ == "__main__":
    create_big_sample_pdf()

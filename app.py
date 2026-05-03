from flask import Flask, render_template, request
from textblob import TextBlob
import nltk
nltk.download('punkt')

app = Flask(__name__)

# AI ANALYSIS FUNCTION
def analyze_answer(text):
    analysis = TextBlob(text)

    # Sentiment
    polarity = analysis.sentiment.polarity
    if polarity > 0.2:
        sentiment = "Positive"
    elif polarity < -0.2:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # Keywords
    keywords = ["team", "project", "lead", "challenge", "problem", "solution"]
    keyword_count = sum(1 for word in keywords if word in text.lower())

    # Confidence logic
    if keyword_count >= 4 and polarity > 0:
        confidence = "High"
    elif keyword_count >= 2:
        confidence = "Medium"
    else:
        confidence = "Low"

    # Score (now correctly placed)
    score = (keyword_count * 15) + (max(polarity, 0) * 50)
    if score > 100:
        score = 100
    score = int(score)

    # Smart feedback
    feedback = ""

    if keyword_count < 2:
        feedback += "Try including more real-world experience keywords. "

    if polarity <= 0:
        feedback += "Your answer feels less confident. Use stronger positive language. "

    if "i" not in text.lower():
        feedback += "Use personal examples (start with 'I did...'). "

    return sentiment, keyword_count, confidence, feedback, score


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        answer = request.form['answer']
        question = request.form['question']

        sentiment, keyword_count, confidence, feedback, score = analyze_answer(answer)

        return render_template(
            'result.html',
            sentiment=sentiment,
            keywords=keyword_count,
            confidence=confidence,
            feedback=feedback,
            score=score,
            question=question
        )

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
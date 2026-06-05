from flask import Flask

app = Flask(__name__)

# 파이썬이 HTML/CSS 코드를 글자(문자열)로 인식하도록 삼중 따옴표(""")로 감싸줍니다.
html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 맞춤형 학습 오답 분석 서비스</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary-color: #ff5a00;
            --bg-color: #f8f9fa;
            --card-bg: #ffffff;
            --text-color: #333333;
        }
        body { font-family: sans-serif; background-color: var(--bg-color); color: var(--text-color); margin: 0; padding: 0; }
        header { background-color: var(--primary-color); color: white; padding: 20px; text-align: center; font-size: 24px; font-weight: bold; }
        .container { max-width: 1000px; margin: 30px auto; padding: 0 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        @media (max-width: 768px) { .container { grid-template-columns: 1fr; } }
        .card { background: var(--card-bg); border-radius: 12px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        h2 { margin-top: 0; color: var(--primary-color); border-bottom: 2px solid #ffe5d4; padding-bottom: 10px; }
        .problem-box { background-color: #f1f3f5; border-left: 5px solid #ced4da; padding: 15px; border-radius: 4px; margin-bottom: 15px; font-weight: 500; }
        .btn-group { display: flex; gap: 10px; margin-top: 15px; }
        button { flex: 1; padding: 12px; border: none; border-radius: 8px; font-size: 15px; font-weight: bold; cursor: pointer; }
        .btn-correct { background-color: #2b8a3e; color: white; }
        .btn-wrong { background-color: #e03131; color: white; }
        #wrong-analysis-section { display: none; margin-top: 20px; background-color: #fff5f5; padding: 15px; border-radius: 8px; border: 1px dashed #ffa8a8; }
        .type-btn { background-color: white; border: 1px solid #ced4da; color: #495057; margin-bottom: 8px; text-align: left; width: 100%; padding: 10px;}
        #feedback-box { display: none; margin-top: 20px; padding: 15px; border-radius: 8px; line-height: 1.6; }
        .bg-concept { background-color: #e7f5ff; border: 1px solid #a5d8ff; }
        .bg-approach { background-color: #fff4e6; border: 1px solid #ffd8a8; }
        .bg-calc { background-color: #f3f0ff; border: 1px solid #d0bfff; }
        .plan-item { display: flex; justify-content: space-between; background: #f8f9fa; padding: 12px; margin-bottom: 8px; border-radius: 6px; border-left: 4px solid var(--primary-color); }
        .badge { background-color: #e9ecef; padding: 3px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <header> QANDA+ (공부 방법 & 오답 분석 가상 시스템) </header>
    <div class="container">
        <div class="card">
            <h2>1. 문제 확인 및 채점</h2>
            <div class="problem-box">
                <strong>[수학 I - 삼각함수]</strong><br>
                문제: 함수 y = sin(2x - π/3)의 주기를 구하시오. (정답: π)
            </div>
            <div class="btn-group">
                <button class="btn-correct" onclick="handleResult(true)">정답입니다 😊</button>
                <button class="btn-wrong" onclick="handleResult(false)">틀렸습니다 😥</button>
            </div>
            <div id="wrong-analysis-section">
                <h3>🔍 AI 분석: 어떤 이유로 틀리셨나요?</h3>
                <button class="type-btn" onclick="provideFeedback('concept')">❌ 개념 오류</button>
                <button class="type-btn" onclick="provideFeedback('approach')">❌ 접근법 오류</button>
                <button class="type-btn" onclick="provideFeedback('calc')">❌ 계산 실수</button>
            </div>
            <div id="feedback-box"></div>
        </div>
        <div class="card">
            <h2>2. 약점 패턴 분석 및 학습 플랜</h2>
            <div style="width:100%; max-width:250px; margin: 0 auto 20px auto;"><canvas id="errorChart"></canvas></div>
            <h3>📅 맞춤 복습 알림 및 추천 플랜</h3>
            <div id="plan-container">
                <div class="plan-item"><span>📚 삼각함수 주기 공식 핵심 요약집 읽기</span><span class="badge" style="color:#228be6;">개념 보완</span></div>
            </div>
        </div>
    </div>
    <script>
        let errorData = { concept: 4, approach: 2, calc: 5 };
        let errorChart;
        function initChart() {
            const ctx = document.getElementById('errorChart').getContext('2d');
            errorChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['개념 오류', '접근법 오류', '계산 실수'],
                    datasets: [{ data: [errorData.concept, errorData.approach, errorData.calc], backgroundColor: ['#a5d8ff', '#ffd8a8', '#d0bfff'] }]
                },
                options: { responsive: true }
            });
        }
        function handleResult(isCorrect) {
            document.getElementById('wrong-analysis-section').style.display = isCorrect ? 'none' : 'block';
            if(isCorrect) {
                let fb = document.getElementById('feedback-box');
                fb.style.display = 'block'; fb.className = 'bg-concept'; fb.innerHTML = '🎉 정답입니다!';
            }
        }
        function provideFeedback(type) {
            let fb = document.getElementById('feedback-box'); fb.style.display = 'block';
            errorData[type]++; errorChart.data.datasets[0].data = [errorData.concept, errorData.approach, errorData.calc]; errorChart.update();
            if(type==='concept') { fb.className = 'bg-concept'; fb.innerHTML = '💡 개념 정리가 필요합니다.'; }
            else if(type==='approach') { fb.className = 'bg-approach'; fb.innerHTML = '💡 유사 유형 패턴 문제집을 추천합니다.'; }
            else { fb.className = 'bg-calc'; fb.innerHTML = '💡 실수를 줄이기 위한 연산 훈련이 필요합니다.'; }
        }
        window.onload = function() { initChart(); };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return html_content

if __name__ == '__main__':
    app.run(debug=True)
    


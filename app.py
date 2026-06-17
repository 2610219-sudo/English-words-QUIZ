import random
from IPython.display import HTML, display, clear_output
import google.colab.output

# 1. 고난도 단어 데이터
단어장 = {
    "inevitable": "피할 수 없는", "ambiguous": "모호한", "comprehensive": "종합적인",
    "subtle": "미묘한", "prevalent": "널리 퍼진", "vulnerable": "취약한",
    "obsolete": "구식의", "spontaneous": "자발적인", "plausible": "그럴듯한",
    "arbitrary": "임의의", "paradox": "역설", "adversary": "상대방"
}

문제들 = list(단어장.keys())
random.shuffle(문제들)
index = 0
오답들 = []

def 채점(답):
    global index, 오답들
    단어 = 문제들[index]
    정답 = 단어장[단어]

    if 답 and (답 in 정답 or 정답 in 답):
        결과 = "정답"
    else:
        결과 = "오답"
        오답들.append(단어)

    # 다음 문제로 넘어가거나 종료하기 위해 index 증가
    index += 1
    화면_업데이트(결과, 정답)


def 화면_업데이트(결과="", 이전정답=""):
    clear_output()

    if index < len(문제들):
        단어 = 문제들[index]
        색상 = "#3498db"
        메시지 = ""

        # 이전 문제 결과에 따른 메시지 생성
        if 결과 == "정답":
            메시지 = f"<div style='color:#2ecc71; margin-bottom:10px;'>✅ 정답입니다! ({이전정답})</div>"
        elif 결과 == "오답":
            메시지 = f"<div style='color:#e74c3c; margin-bottom:10px;'>❌ 오답 (정답: {이전정답})</div>"

        # HTML/CSS 디자인 (카드 안에 입력창 포함)
        html_code = f"""
        <div style="font-family:sans-serif; max-width:400px; margin:20px auto; padding:30px;
                    border-radius:20px; background: white; border:4px solid {색상}; text-align:center; box-shadow:0 10px 20px rgba(0,0,0,0.1);">
            <div style="font-size:12px; color:#95a5a6; margin-bottom:10px;">PROGRESS: {index+1}/{len(문제들)}</div>
            <h1 style="font-size:40px; color:#2c3e50; margin-bottom:20px;">{단어}</h1>
            {메시지}
            <input type="text" id="answer_box" style="width:80%; padding:10px; border-radius:10px; border:2px solid #ddd; font-size:16px; text-align:center;" placeholder="뜻을 입력하세요" onkeydown="if(event.keyCode==13) submit_answer()">
            <button onclick="submit_answer()" style="margin-top:15px; padding:10px 20px; background:{색상}; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold; width:87%;">확인 (Enter)</button>
        </div>
        <script>
            function submit_answer() {{
                var val = document.getElementById('answer_box').value;
                google.colab.kernel.invokeFunction('채점_함수', [val], {{}});
            }}
            document.getElementById('answer_box').focus();
        </script>
        """
        display(HTML(html_code))
    else:
        # 모든 문제를 풀었을 때의 종료 화면
        display(HTML(f"""
        <div style="text-align:center; padding:50px; font-family:sans-serif;">
            <h1>🏆 학습 완료!</h1>
            <p style="font-size:16px; margin:20px 0;">틀린 단어: {', '.join(set(오답들)) if 오답들 else '없음'}</p>
            <button onclick="google.colab.kernel.invokeFunction('재시작_함수', [], {{}})" style="padding:10px 20px; border:none; background:#3498db; color:white; border-radius:10px; cursor:pointer; font-weight:bold;">다시 시작</button>
        </div>
        """))

def 재시작():
    global index, 오답들, 문제들
    random.shuffle(문제들)
    index = 0
    오답들 = []
    화면_업데이트()

# 파이썬 함수와 자바스크립트 연결
google.colab.output.register_callback('채점_함수', 채점)
google.colab.output.register_callback('재시작_함수', 재시작)

# 첫 화면 실행
화면_업데이트()

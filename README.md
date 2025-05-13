# Upbit Surge Predictor

업비트 원화마켓을 대상으로 한 **선행급등포착 자동 추천 시스템**입니다.  
체결강도, 호가 잔량, 거래대금 등 실시간 조건을 기반으로  
**10분 내 3% 이상 상승 가능성이 높은 코인**을 포착하여  
텔레그램으로 자동 전송합니다.

---

## ✅ 사용 방법

### 1. 설정
`config.json` 파일에 아래 정보를 입력하세요:

```json
{
  "TELEGRAM_BOT_TOKEN": "당신의 텔레그램 봇 토큰",
  "TELEGRAM_CHAT_ID": "대상 채팅방 ID"
}
```

### 2. 실행

```bash
python main.py
```

또는 Docker 환경에서:

```bash
docker build -t upbit-bot .
docker run upbit-bot
```

---

## 🐳 Koyeb 배포
Dockerfile이 포함되어 있으므로 바로 Koyeb에서 `GitHub 연결 → 배포` 가능  
`main.py` 자동 실행됩니다.

---

## 📩 메시지 예시
```
[선행급등포착]
- 코인명: KRW-SAND
- 현재가: 784원
- 매수 추천가: 780 ~ 790원
- 목표 매도가: 807원
- 예상 수익률: 3%
- 예상 소요 시간: 10분 내
- 추천 이유: 매수세 급증 + 호가 우위 포착
```

---

## 📁 구성 파일

| 파일명 | 설명 |
|--------|------|
| `main.py` | 코어 로직 실행 파일 |
| `config.json` | 토큰/채팅 ID 설정 |
| `Dockerfile` | 컨테이너 실행용 설정 |
| `requirements.txt` | 의존성 패키지 목록 |

---

## 👨‍💻 개발자
- GitHub: [lee0257](https://github.com/lee0257)

---
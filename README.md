# ♻️ VILLAGE DL

이 저장소는 [YOLO] 객체 탐지 프레임워크를 활용해 쓰레기를 인식하는 실험을 담고 있습니다. 
학습된 모델을 간단한 Flask API로 감싸 이미지 파일을 전송하면 탐지된 객체 정보를 JSON으로 반환합니다.

## 📂 프로젝트 구조

| 경로 | 설명 |
| ---- | ---- |
| `app.py` | `/detect`와 `/crawler` 엔드포인트를 제공하는 Flask 애플리케이션 |
| `best.pt` | 재활용품 데이터셋으로 학습한 YOLO 가중치 |
| `merged_dataset.yaml` | **can**, **glass**, **paper** 등 클래스를 정의한 데이터셋 설정 파일 |
| `train.ipynb` | 모델 학습에 사용한 Jupyter Notebook |
| `predict.ipynb` | 예시 이미지로 추론을 수행하는 Notebook |
| `prepare_dataset.ipynb` | 데이터셋 준비 및 병합 과정 Notebook |

## ⚙️ 설치 방법

1. (선택) 가상 환경을 생성하고 활성화합니다.
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. 필요한 라이브러리를 설치합니다.
   ```bash
   pip install flask flask-cors ultralytics pillow
   ```

## ▶️ API 실행

Flask 애플리케이션을 실행합니다.
```bash
flask run --debug
```

API는 다음의 두 엔드포인트를 제공합니다.

- `POST /detect`
  - 요청: `multipart/form-data` 형식으로 `file` 필드에 이미지를 포함
  - 응답: `[x1, y1, x2, y2, confidence, class_id, class_name]` 형태의 바운딩 박스 리스트

- `POST /crawler`
  - 요청: 다음 필드를 포함한 JSON 객체
    - `url`: 크롤링을 시작할 URL
    - `linkSelector`, `titleSelector`, `dateSelector`, `contentSelector`: 파싱에 사용할 CSS 셀렉터
    - `urlPrefix`: 상대 경로 보정을 위한 선택적 접두사
    - `keywords`: 결과를 필터링할 키워드 목록
  - 응답: 커스텀 크롤러가 추출한 항목

## 📊 데이터셋

YOLO 모델은 `merged_dataset.yaml`에 정의된 병합 데이터셋으로 학습되었습니다. 
이 데이터셋은 캔, 종이, 플라스틱, 비닐 등 7개의 재활용 품목 클래스를 포함합니다.

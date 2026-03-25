import nbformat as nbf
import os

def append_closing_md(path, closing_md):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)
    
    closing_cell = nbf.v4.new_markdown_cell(closing_md)
    nb.cells.append(closing_cell)
    
    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

closing_md = """## 🤖 5. 머신러닝 예측 모델 (Machine Learning Models) 요약
- **Logistic Regression**: 기본 가중치 파악용 선형 베이스라인 모델
- **Random Forest & XGBoost**: 복잡한 상호작용 포착용 고도화 앙상블 모델

## 📁 6. 프로젝트 산출물 안내 (Project Assets)
- `models/`: 학습 완료된 모델 파일 (*.joblib)
- `results/plots/`: 논문용 고해상도 이미지 (01~07 PNG)
"""

append_closing_md(r'c:\Users\parks\Desktop\dust\HealthImpactVisualizations.ipynb', closing_md)
append_closing_md(r'c:\Users\parks\Desktop\dust\Model_Training.ipynb', closing_md)
print("Closing sections appended.")

import nbformat as nbf
import os

def rewrite_notebook_docs(path, intro_md, proof_updates):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    
    with open(path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)
    
    # 1. Update/Add Intro (Overview & Hypotheses)
    # Check if a markdown cell at the top already has similar content or replace the very first cell
    intro_cell = nbf.v4.new_markdown_cell(intro_md)
    nb.cells.insert(0, intro_cell)
    
    # 2. Update Proof cells
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            content = "".join(cell.source)
            for key, new_source in proof_updates.items():
                if key in content:
                    cell.source = new_source
                    print(f"Matched and updated proof cell for {key}")
                    
    with open(path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

# Common Intro from README
intro_md = """# 😷 개인별 건강 취약성 및 방어 행동을 고려한 맞춤형 건강 영향 등급 예측 모델

## 📖 1. 프로젝트 개요 (Context & Problem Statement)
현재 국가 단위의 미세먼지 예보 시스템은 대기 중 오염 물질의 농도(AQI 등)중심으로 일괄적인 정보만을 제공하고 있습니다. 개인이 실제로 느끼는 건강 위험은 연령, 기저질환, 마스크 착용 유무 등에 따라 달라지므로, 본 프로젝트는 **개별적 취약성과 방어 행동을 모델링하여 맞춤형 건강 심각도(Health Impact Class)를 예측**합니다.

## 🎯 2. 핵심 가설 (Hypothesis)
1. **거시적 지표와 미시적 노출의 결합**: 동일한 AQI 상태더라도 도로와의 거리가 가까울수록 초국소적 오염원 노출로 인해 위험 등급이 상승할 것이다.
2. **생물학적 취약성 층화**: 취약 계층(고령자, 환자)은 일반인보다 더 낮은 오염 농도에서도 위험 등급이 급격히 상승하는 임계치를 가질 것이다.
3. **방어 행동의 상쇄 효과**: 고농도 노출 환경에서도 마스크 착용 등의 적극적 행동은 최종 위험 등급을 낮추는 실질적인 방어기제로 작동할 것이다.
"""

# HIV specific proofs
hiv_proofs = {
    "[증명 1]": [
        "### [증명 1] 연령대별 AQI 대비 건강 위험도 (Scatter/Box Plot)\n",
        "![연령대별 분석](results/plots/01_age_group_boxplot.png)\n",
        "**[무엇을 증명하는가?]** \"동일한 공기질에서도 나이 든 사람은 더 위험하다\"는 사실을 입증합니다. 연령대에 따라 건강 점수가 상하로 뚜렷하게 나뉘는 층화 현상을 보여줍니다."
    ],
    "[증명 2]": [
        "### [증명 2] 방어 행동에 따른 위험 상쇄 효과 (Box Plot)\n",
        "![마스크 착용 효과](results/plots/02_mask_usage_boxplot.png)\n",
        "**[무엇을 증명하는가?]** \"마스크가 진짜 효과가 있는가?\"를 입증합니다. 마스크 착용 그룹의 위험 등급 분포가 미착용 그룹보다 전체적으로 낮게 형성됨을 시각화합니다."
    ],
    "[증명 3]": [
        "### [증명 3] 변수 간 상관관계 히트맵 (Correlation Matrix)\n",
        "![상관관계 히트맵](results/plots/04_correlation_heatmap.png)\n",
        "**[무엇을 증명하는가?]** \"각 변수들이 결과에 원인을 제공하는가?\"를 통계적으로 입증합니다. 변수들 간의 연관성을 계수로 보여주어 데이터 설계의 타당성을 증명합니다."
    ]
}

# MT specific proofs
mt_proofs = {
    "[증명 4]": [
        "### [증명 4] 트리 기반 특성 중요도 (Feature Importance)\n",
        "![특성 중요도 분석](results/plots/03_feature_importance.png)\n",
        "**[무엇을 증명하는가?]** \"어떤 요인이 예측에 가장 결정적인가?\"를 증명합니다. 미세먼지 수치보다 때로는 기저질환이나 마스크 착용이 위험도 예측에 더 큰 영향을 미침을 순위로 보여줍니다."
    ],
    "[증명 5]": [
        "### [증명 5] 다중 클래스 ROC 커브 및 AUC\n",
        "![ROC-AUC 성능](results/plots/05_roc_auc_curve.png)\n",
        "**[무엇을 증명하는가?]** \"모델의 판정이 얼마나 정확하고 신뢰할만한가?\"를 증명합니다. 0~4등급을 구분함에 있어 오판 확률이 얼마나 낮은지를 면적(AUC) 수치로 입증합니다."
    ],
    "[증명 6]": [
        "### [증명 6] XGBoost SHAP Value 요약 플롯 (XAI)\n",
        "![SHAP 기여도 분석](results/plots/06_shap_summary.png)\n",
        "**[무엇을 증명하는가?]** \"모델이 왜 그런 판정을 내렸는가?\"를 투명하게 증명합니다. 특정 변수(예: 도로 거리)가 위험 등급을 어느 방향(상승/하락)으로 얼마나 강력하게 밀어냈는지 낱낱이 보여줍니다."
    ],
    "[증명 7]": [
        "### [증명 7] 데이터 양에 따른 학습 곡선 (Learning Curve)\n",
        "![학습 곡선](results/plots/07_learning_curve.png)\n",
        "**[무엇을 증명하는가?]** \"모델이 과적합(암기) 없이 제대로 학습되었는가?\"를 증명합니다. 데이터가 늘어남에 따라 훈련과 검증 정확도가 수렴하는 과정을 보여주어 모델의 일반화 능력을 입증합니다."
    ]
}

rewrite_notebook_docs(r'c:\Users\parks\Desktop\dust\HealthImpactVisualizations.ipynb', intro_md, hiv_proofs)
rewrite_notebook_docs(r'c:\Users\parks\Desktop\dust\Model_Training.ipynb', intro_md, mt_proofs)
print("Documentation synchronization complete.")

import streamlit as st
import pandas as pd

# 2026年基準
CURRENT_YEAR = 2026
DEPRECIATION_RATE = 0.008  # 建物老朽化による賃料下落率 (年0.8%)

# --- 1. ページ設定 ---
st.set_page_config(page_title="不動産出口戦略シミュレーター", layout="centered")

# デザイン調整
st.markdown("""
    <style>
    header[data-testid="stHeader"] { visibility: hidden; display: none; }
    footer { visibility: hidden; }
    .stApp { background-color: #f8fafc; }
    .center-container { display: flex; justify-content: center; width: 100%; margin: 30px 0; }
    div.stButton > button {
        min-width: 340px !important; height: 60px !important; font-size: 22px !important;
        font-weight: bold !important; background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        color: white !important; border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important; border: none !important;
    }
    .prediction-card {
        background: white; padding: 20px; border-radius: 12px;
        border-top: 6px solid #334155; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px; text-align: center;
    }
    .pred-label { color: #64748b; font-weight: bold; font-size: 0.9rem; }
    .pred-price { color: #1e293b; font-size: 1.8rem; font-weight: bold; margin: 5px 0; }
    .pred-diff { font-size: 0.95rem; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 入力フォーム ---
st.title("🏦 不動産出口戦略シミュレーション")
st.subheader("〜 手入力データに基づく計算モデル 〜")

with st.container():
    mansion_name = st.text_input("物件名 (任意)", placeholder="例：代官山レジデンス")
    
    col1, col2 = st.columns(2)
    with col1:
        price_now = st.number_input("現在の物件価格 (万円)", min_value=100, value=8000, step=100)
        rent_now = st.number_input("現在の月額賃料 (円)", min_value=1000, value=250000, step=1000)
    with col2:
        area = st.number_input("専有面積 (㎡)", min_value=10.0, value=60.0, step=0.1)
        year_built = st.number_input("築年 (西暦)", min_value=1970, max_value=2026, value=2015)

st.markdown('<div class="center-container">', unsafe_allow_html=True)
clicked = st.button("　将来価値を計算する　")
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. 計算ロジック & 表示 ---
if clicked:
    # 表面利回り
    yield_now = (rent_now * 12) / (price_now * 10000) * 100

    # 将来価格計算関数 (市場上昇率と経年変化)
    def calc_future_price(years, market_growth_rate):
        # 簡易モデル: 市場上昇率を反映
        return price_now * ((1 + market_growth_rate) ** years)

    # 5年後・10年後のシナリオ（年率 1%, 3%, 5% 上昇想定）
    p_5y = [calc_future_price(5, r) for r in [0.01, 0.03, 0.05]]
    p_10y = [calc_future_price(10, r) for r in [0.01, 0.03, 0.05]]

    def get_diff_html(future, current):
        diff = round((future / current - 1) * 100, 1)
        color = "#e11d48" if diff >= 0 else "#2563eb"
        sign = "+" if diff >= 0 else ""
        return f'<span style="color: {color}; font-weight: bold;">{sign}{diff}%</span>'

    st.divider()
    
    # 基本指標表示
    c1, c2, c3 = st.columns(3)
    c1.metric("想定表面利回り", f"{yield_now:.2f} %")
    c2.metric("平米単価 (現在)", f"{int(price_now / area):,} 万円/㎡")
    c3.metric("月額賃料単価", f"{int(rent_now / area):,} 円/㎡")

    # 売却価格シナリオ
    st.write("### 📅 5年後の予想売却価格")
    cols_5 = st.columns(3)
    labels = ["保守的 (年1%)", "標準的 (年3%)", "積極的 (年5%)"]
    for i, col in enumerate(cols_5):
        with col:
            st.markdown(f'''
                <div class="prediction-card">
                    <div class="pred-label">{labels[i]}</div>
                    <div class="pred-price">{int(p_5y[i]):,} 万円</div>
                    <div class="pred-diff">価格推移 {get_diff_html(p_5y[i], price_now)}</div>
                </div>
            ''', unsafe_allow_html=True)

    st.write("### 📅 10年後の予想売却価格")
    cols_10 = st.columns(3)
    for i, col in enumerate(cols_10):
        with col:
            st.markdown(f'''
                <div class="prediction-card">
                    <div class="pred-label">{labels[i]}</div>
                    <div class="pred-price">{int(p_10y[i]):,} 万円</div>
                    <div class="pred-diff">価格推移 {get_diff_html(p_10y[i], price_now)}</div>
                </div>
            ''', unsafe_allow_html=True)

    # 賃料の将来推移（老朽化下落を加味）
    st.write("---")
    st.write("### 🏠 賃料の将来予測 (インフレ vs 経年劣化)")
    
    def calc_future_rent(years, inflation_rate):
        # 賃料 = ベース賃料 * (1 - 劣化率)^年数 * (1 + インフレ率)^年数
        return rent_now * ((1 - DEPRECIATION_RATE)**years) * ((1 + inflation_rate)**years)

    r10_1 = calc_future_rent(10, 0.01)
    r10_2 = calc_future_rent(10, 0.02)

    rc1, rc2, rc3 = st.columns(3)
    rc1.metric("現在の賃料", f"{int(rent_now):,} 円")
    rc2.metric("10年後 (インフレ1%)", f"{int(r10_1):,} 円")
    rc3.metric("10年後 (インフレ2%)", f"{int(r10_2):,} 円")
    
    st.caption(f"※経年劣化による賃料下落を年{DEPRECIATION_RATE*100}%と仮定して算出")

    # 戦略パッケージ
    st.write("### 💰 売却価格戦略")
    st.table(pd.DataFrame({
        "項目": ["売出目標 (強気)", "適正成約ライン", "早期売却下限"],
        "金額": [f"{int(price_now * 1.1):,} 万円", f"{int(price_now):,} 万円", f"{int(price_now * 0.93):,} 万円"],
        "根拠": ["相場+10%からのスタート", "入力された基準価格", "仲介手数料+アルファ引"]
    }))

st.markdown("---")
st.caption("※本アプリは入力された数値に基づく計算シミュレーションであり、将来の価値を保証するものではありません。")

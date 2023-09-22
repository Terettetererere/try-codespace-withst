# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
# from streamlit.logger import get_logger

# LOGGER = get_logger(__name__)


def run():
    # アプリのタイトル
    st.title("積立投資シミュレーションアプリ")

    # スライダーを追加
    st.sidebar.header("パラメータ設定")
    years = st.sidebar.slider("想定年数", 1, 30, 10)
    annual_interest_rate = st.sidebar.slider("利回り（年率）", 0.1, 30.0, 5.0, step=0.1)
    monthly_investment = st.sidebar.slider("積立額", 1000, 100000, 20000, step=1000)
    initial_investment = st.sidebar.slider("初期投資額", 0, 100000, 10000, step=10000)

    # 複利計算用の月利率
    monthly_interest_rate = (annual_interest_rate / 100) / 12

    time_period = np.arange(years * 12 + 1)
    investment_values = []
    total_contributions = []

    for month in time_period:
        if month == 0:
            investment = initial_investment + monthly_investment # 初月の積立元本は初期投資額
        else:
            investment = investment_values[-1] * (1 + monthly_interest_rate) + monthly_investment
        investment_values.append(investment)
        total_contribution = initial_investment + sum(monthly_investment for _ in range(month))
        total_contributions.append(total_contribution)

    dt = pd.DataFrame(columns=['Increase', 'Investment'])
    dt['Increase'] = investment_values
    dt['Investment'] = total_contributions
    #st.write(dt)

    # プロット
    fig, ax = plt.subplots()
    ax.bar(time_period, investment_values, label="Increase", color="blue")
    ax.bar(time_period, np.array(total_contributions), label="Investment", color="green")
    ax.set_xlabel("year")
    ax.set_ylabel("money")
    ax.set_title("Simulation")
    ax.legend()
    # グラフを表示
    st.pyplot(fig)

    # プロット
    fig = px.bar(x=time_period, y=[investment_values, total_contributions],
                labels={"y": "money", "x": "year"},
                title="Simulation")
    fig.update_traces(marker_color=["blue", "green"])
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.update_xaxes(title_text="year")
    fig.update_yaxes(title_text="money")
    st.plotly_chart(fig)

    # プロット
    fig = px.bar(dt, x=time_period, y=['Increase', 'Investment'],
                #hover_name=['Increase', 'Investment'],
                title="積立投資シミュレーション",
                color_discrete_sequence=["blue", "green"],
                barmode="overlay",
                opacity=1
                )
    fig.update_xaxes(title_text="期間")
    fig.update_yaxes(title_text="金額")
    st.plotly_chart(fig)


if __name__ == "__main__":
    run()

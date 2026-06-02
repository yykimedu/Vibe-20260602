import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt

# 웹에서 타이타닉 데이터셋 다운로드
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

df = pd.read_csv(url)

# 성별 생존 비율 계산
survival_by_sex = df.groupby("Sex")["Survived"].mean() * 100

print("=== 성별 생존 비율 ===")
print(survival_by_sex.round(2).astype(str) + "%")

# 바차트 그리기
fig, ax = plt.subplots(figsize=(8, 5))
bar_colors = ["#4c72b0", "#dd8452"]

survival_by_sex.plot(
    kind="bar",
    color=bar_colors,
    edgecolor="black",
    ax=ax,
)

ax.set_title("Titanic Survival Rate by Gender", fontsize=16)
ax.set_xlabel("Gender", fontsize=12)
ax.set_ylabel("Survival Rate (%)", fontsize=12)
ax.set_ylim(0, 100)
ax.set_xticklabels(["female", "male"], rotation=0)

for p in ax.patches:
    ax.annotate(
        f"{p.get_height():.1f}%",
        (p.get_x() + p.get_width() / 2, p.get_height()),
        ha="center",
        va="bottom",
        fontsize=11,
        color="black",
        xytext=(0, 5),
        textcoords="offset points",
    )

plt.tight_layout()
plt.savefig("titanic_survival_by_gender.png", dpi=150)
print("Saved titanic_survival_by_gender.png")

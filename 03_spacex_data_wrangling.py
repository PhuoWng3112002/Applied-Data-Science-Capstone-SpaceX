import pandas as pd
import numpy as np

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")

# Thống kê số lượng theo bãi phóng, quỹ đạo và kết quả hạ cánh
print(df['LaunchSite'].value_counts())
print(df['Orbit'].value_counts())
landing_outcomes = df['Outcome'].value_counts()
print(landing_outcomes)

# Xác định các trạng thái hạ cánh thất bại
bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])

# Tạo biến mục tiêu Class (1 = Thành công, 0 = Thất bại)
landing_class = [0 if outcome in bad_outcomes else 1 for outcome in df['Outcome']]
df['Class'] = landing_class

print("Success rate:", df["Class"].mean())
df.to_csv("dataset_part_2.csv", index=False)
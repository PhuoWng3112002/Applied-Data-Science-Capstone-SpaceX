import sqlite3
import pandas as pd

con = sqlite3.connect("my_data1.db")
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False, method="multi")

queries = [
    # 1. Danh sách bãi phóng duy nhất
    "SELECT DISTINCT Launch_Site FROM SPACEXTBL;",
    # 2. 5 bản ghi đầu có bãi phóng bắt đầu bằng 'CCA'
    "SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5;",
    # 3. Tổng khối lượng tải trọng của NASA (CRS)
    "SELECT SUM(PAYLOAD_MASS__KG_) AS Total_NASA_Payload FROM SPACEXTBL WHERE Customer = 'NASA (CRS)';",
    # 4. Tải trọng trung bình của F9 v1.1
    "SELECT AVG(PAYLOAD_MASS__KG_) AS Avg_Payload_F9_v11 FROM SPACEXTBL WHERE Booster_Version = 'F9 v1.1';",
    # 5. Ngày hạ cánh thành công đầu tiên trên mặt đất (RTLS)
    "SELECT MIN(Date) AS First_RTLS_Success FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)';",
    # 6. Tên booster hạ cánh thành công trên drone ship với tải trọng 4000-6000 kg
    "SELECT Booster_Version FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000;",
    # 7. Tổng số nhiệm vụ thành công và thất bại
    "SELECT Mission_Outcome, COUNT(*) AS Total FROM SPACEXTBL GROUP BY Mission_Outcome;",
    # 8. Booster mang tải trọng lớn nhất
    "SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);",
    # 9. Các vụ hạ cánh thất bại trên drone ship năm 2015
    "SELECT substr(Date, 6, 2) AS Month, Landing_Outcome, Booster_Version, Launch_Site FROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)' AND substr(Date, 0, 5) = '2015';",
    # 10. Xếp hạng số lượng kết quả hạ cánh từ 2010-06-04 đến 2017-03-20
    "SELECT Landing_Outcome, COUNT(*) AS Outcome_Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Outcome_Count DESC;"
]

for i, q in enumerate(queries, 1):
    print(f"--- Query {i} ---")
    print(pd.read_sql_query(q, con))
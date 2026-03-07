import os
from PIL import Image
import matplotlib.pyplot as plt
from model import detect_food


# 이미지 경로
image_path = "sample_images/test1.png"

image = Image.open(image_path).convert("RGB")


# 모델 실행
result_image = detect_food(image)


# 저장
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "result_example.png")

result_image.save(output_path)

print(f"결과 이미지 저장 완료: {output_path}")


# 시각화
plt.figure(figsize=(10, 10))
plt.imshow(result_image)
plt.axis("off")
plt.show()
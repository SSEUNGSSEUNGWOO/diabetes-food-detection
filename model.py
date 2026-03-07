import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import AutoImageProcessor, AutoModelForObjectDetection


# 모델 로드
processor = AutoImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = AutoModelForObjectDetection.from_pretrained("facebook/detr-resnet-50")


# 음식 위험도 정의
food_list = {
    "cake": "Dangerous",
    "hot dog": "Dangerous",
    "pizza": "Dangerous",
    "donut": "Dangerous",
    "sandwich": "Dangerous",
    "banana": "Caution",
    "orange": "Caution",
    "pear": "Caution",
    "apple": "Safe",
    "carrot": "Safe",
    "broccoli": "Safe"
}

color_map = {
    "Dangerous": "red",
    "Caution": "yellow",
    "Safe": "green"
}


def detect_food(image):
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(
        outputs,
        target_sizes=target_sizes
    )[0]

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", size=26)

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        label_name = model.config.id2label[label.item()]

        if score < 0.8:
            continue

        if label_name not in food_list:
            continue

        danger_level = food_list[label_name]
        color = color_map[danger_level]

        box = [int(x) for x in box.tolist()]
        draw.rectangle(box, outline=color, width=5)

        text = f"{label_name} ({danger_level})"

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = box[0]
        text_y = max(0, box[1] - text_height - 8)

        text_bg = [
            text_x,
            text_y,
            text_x + text_width + 6,
            text_y + text_height + 4
        ]

        draw.rectangle(text_bg, fill=color)

        text_color = "black" if danger_level == "Caution" else "white"
        draw.text((text_x + 3, text_y + 2), text, fill=text_color, font=font)

    return image
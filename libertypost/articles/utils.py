from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile


def process_cover_image(uploaded_file):
    image = Image.open(uploaded_file)

    target_ratio = 665 / 300

    max_width = 1920
    max_height = int(max_width / target_ratio)

    orig_width, orig_height = image.size

    if orig_width > max_width or orig_height > max_height:
        target_width, target_height = max_width, max_height
    else:
        if orig_width / orig_height > target_ratio:
            target_height = orig_height
            target_width = int(target_height * target_ratio)
        else:
            target_width = orig_width
            target_height = int(target_width / target_ratio)

    scale_x = target_width / orig_width
    scale_y = target_height / orig_height
    scale = max(scale_x, scale_y)

    new_width = int(orig_width * scale)
    new_height = int(orig_height * scale)
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    image = image.crop((left, top, left + target_width, top + target_height))

    output = io.BytesIO()
    image.save(output, format="JPEG", quality=90)
    output.seek(0)

    return InMemoryUploadedFile(
        output,
        "ImageField",
        f"processed_{uploaded_file.name.split('.')[0]}.jpg",
        "image/jpeg",
        output.getbuffer().nbytes,
        None,
    )

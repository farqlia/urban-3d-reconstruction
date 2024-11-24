import argparse
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

def merge_and_annotate_images(ground_truth_path, predicted_path, output_path):
    # Load images
    ground_truth = Image.open(ground_truth_path)
    predicted = Image.open(predicted_path)

    # Ensure both images have the same size
    if ground_truth.size != predicted.size:
        predicted = predicted.resize(ground_truth.size)

    # Merge images side by side
    merged_width = ground_truth.width + predicted.width
    merged_height = ground_truth.height
    merged_image = Image.new("RGB", (merged_width, merged_height))

    # Paste images
    merged_image.paste(ground_truth, (0, 0))
    merged_image.paste(predicted, (ground_truth.width, 0))

    # Annotate images
    draw = ImageDraw.Draw(merged_image)
    font_size = 20
    try:
        # Try loading a default font for better customization
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fallback to default PIL font
        font = ImageFont.load_default()

    text_width = int(5.5 * font_size)
    text_height = int(3.5 * font_size)
    padding = 10
    '''
    # Ground Truth annotation
    gt_text = "Real"

    gt_position = (padding, padding)  # Top-right corner of the first image
    draw.multiline_text(gt_position, gt_text, fill="white", font=font)

    # Predicted annotation
    pred_text = "Predicted"
    pred_position = (ground_truth.width + padding, padding)  # Top-right corner of the second image
    draw.text(pred_position, pred_text, fill="white", font=font)
    '''

    # Save the merged and annotated image
    merged_image.save(output_path)
    print(f"Merged and annotated image saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate rendered images against real ones.")

    parser.add_argument("--render_dir", type=str, required=True, help='Path to the directory of rendered images.')
    parser.add_argument("--real_dir", type=str, required=True, help='Path to the directory of real images.')
    parser.add_argument("--output_dir", type=str, required=True, help='Path to save images with metrics overlay.')

    args = parser.parse_args()

    render_dir = Path(args.render_dir)
    real_dir = Path(args.real_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    n = len(os.listdir(render_dir))

    for i, name in enumerate(zip([f"eval_with_metrics_{i:04d}.png" for i in range(n)], [f"img_{i:04d}.png" for i in range(n)])):
        pred_img_path = render_dir / name[0]
        real_img_path = real_dir / name[1]

        # Define output path
        output_path = output_dir / f"merged_{i:04d}.png"

        # Save image with metrics overlay
        merge_and_annotate_images(real_img_path, pred_img_path, output_path)
import argparse
import os
from pathlib import Path
import imageio.v2 as imageio
import torch
from torchmetrics import StructuralSimilarityIndexMeasure, PeakSignalNoiseRatio
from torchmetrics.image.lpip import LearnedPerceptualImagePatchSimilarity
from PIL import Image, ImageDraw, ImageFont

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
SSIM = StructuralSimilarityIndexMeasure(data_range=1.0).to(device)
PSNR = PeakSignalNoiseRatio(data_range=1.0).to(device)
LPIPS = LearnedPerceptualImagePatchSimilarity(net_type="alex", normalize=True).to(device)


def compute_metrics(pred_img, real_img):
    pred = torch.tensor(imageio.imread(pred_img) / 255.0).type(torch.float32).to(device)[None, ...]
    real = torch.tensor(imageio.imread(real_img) / 255.0).type(torch.float32).to(device)[None, ...]

    pred_p = pred.permute(0, 3, 1, 2)  # [1, 3, H, W]
    real_p = real.permute(0, 3, 1, 2)  # [1, 3, H, W]
    return PSNR(pred_p, real_p).item(), SSIM(pred_p, real_p).item(), LPIPS(pred_p, real_p).item()


def save_image_with_metrics(pred_img_path, output_path, psnr, ssim, lpips):
    # Load the predicted image
    image = Image.open(pred_img_path)
    draw = ImageDraw.Draw(image)

    # Prepare the text to display
    text = f"PSNR: {psnr:.2f}\nSSIM: {ssim:.2f}\nLPIPS: {lpips:.2f}"

    # Optional: Specify a font and size
    size = 32
    font = ImageFont.load_default(size)

    # Calculate text size manually by splitting lines
    text_width = int(5.5 * size)
    text_height = int(3.5 * size)
    padding = 10

    # Define the position and size of the background rectangle
    background_position = (10, 10, 10 + text_width + padding, 10 + text_height + padding)

    # Draw black rectangle as background
    draw.rectangle(background_position, fill="black")

    # Draw the text on top of the black background
    text_position = (10 + padding // 2, 10 + padding // 2)
    draw.multiline_text(text_position, text, fill="white", font=font)

    # Save the image with metrics overlay
    image.save(output_path)


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

    for i, name in enumerate(zip([f"eval_{i:04d}.png" for i in range(n)], [f"img_{i:04d}.png" for i in range(n)])):
        pred_img_path = render_dir / name[0]
        real_img_path = real_dir / name[1]

        # Compute metrics
        psnr, ssim, lpips = compute_metrics(pred_img_path, real_img_path)
        print(f"Image {name[1]} metrics: PSNR = {psnr:.3f}, SSIM = {ssim:.3f}, LPIPS = {lpips:.3f}")

        # Define output path
        output_path = output_dir / f"eval_with_metrics_{i:04d}.png"

        # Save image with metrics overlay
        save_image_with_metrics(pred_img_path, output_path, psnr, ssim, lpips)

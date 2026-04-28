from PIL import Image

if __name__ == '__main__':
    # Open the source image
    with Image.open("Aubot.png") as img:
        # Set your desired size
        new_size = (16, 16)

        # Resize with high-quality resampling
        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Save the result
        resized_img.save("icon16.png")
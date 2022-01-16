from utils import get_image_paths


if __name__ == "__main__":
    image_paths = get_image_paths("./images/task_images")
    print(sorted(image_paths))

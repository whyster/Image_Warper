import image_tools, argparse


# def parse_args():
#     return args


def main():
    while True:
        image = image_tools.ToolsImage.from_image_path('image.jpg')
        image.slice_offset(offset=60, preview=True)
    raise NotImplementedError


if __name__ == '__main__':
    main()

import cv2
import numpy as np
import os
import argparse

class PNG_to_PLT_Converter:
    def __init__(self, block_size, gap, qr_grid_factor, remove_border):
        self.block_size = block_size
        self.gap = gap
        self.qr_grid_factor = qr_grid_factor
        self.remove_border = remove_border

    def remove_white_border(self, image_path):
        if not self.remove_border:
            return cv2.imread(image_path)

        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
            cropped_image = image[y:y + h, x:x + w]
            return cropped_image

        return image

    def png_to_plot(self, input_path, output_path):
        cropped_qr_code_path = 'cropped_qr_code.png'

        if self.remove_border:
            cropped_qr_code = self.remove_white_border(input_path)
            cv2.imwrite(cropped_qr_code_path, cropped_qr_code)
        else:
            cropped_qr_code = cv2.imread(input_path)

        image = cv2.imread(cropped_qr_code_path, cv2.IMREAD_GRAYSCALE)

        # calculates the qr code grid size
        height, width = image.shape
        qr_grid_size = int(height / self.qr_grid_factor)

        block_size = height // qr_grid_size
        qr_code_data = []

        for row in reversed(range(qr_grid_size)):
            for col in range(qr_grid_size):
                x1, y1 = col * block_size, row * block_size
                x2, y2 = x1 + block_size, y1 + block_size
                block = image[y1:y2, x1:x2]
                mean_color = cv2.mean(block)[0]
                qr_code_data.append(1 if mean_color < 128 else 0)

        block_data = qr_code_data
        x_range = qr_grid_size * (self.block_size + self.gap)
        y_range = qr_grid_size * (self.block_size + self.gap)
        x_block = -0.5 * x_range
        y_block = -0.5 * y_range
        plt_commands = ["IN;\n"]

        for i, value in enumerate(block_data):
            if value == 1:
                for y in range(int(y_block), int(y_block + self.block_size)):
                    plt_commands.append(f"PU;PA{x_block},{y};PD;PA{x_block + self.block_size},{y};\n")

            x_block += self.block_size + self.gap

            if (i + 1) % qr_grid_size == 0:
                x_block = -0.5 * x_range
                y_block += self.block_size + self.gap

        plt_commands.append("PU;")
        os.remove(cropped_qr_code_path)

        with open(output_path, "w") as plt_file:
            plt_file.write("".join(plt_commands))

def main():
    parser = argparse.ArgumentParser(description="Convert a .png image to a .plt file.")
    parser.add_argument("input_file", help="Path to the input .png file.")
    parser.add_argument("output_file", help="Path to the output .plt file.")
    args = parser.parse_args()

    block_size = 10
    gap = 4
    qr_grid_factor = 6
    remove_border = True
    converter = PNG_to_PLT_Converter(block_size, gap, qr_grid_factor, remove_border)
    converter.png_to_plot(args.input_file, args.output_file)

if __name__ == "__main__":
    main()      
    
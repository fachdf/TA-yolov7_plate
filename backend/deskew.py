import aspose.pycore as aspycore
from aspose.imaging import Image, RasterImage, Color
import os


if 'TEMPLATE_DIR' in os.environ:
	templates_folder = os.environ['TEMPLATE_DIR']
else:
	templates_folder = "data_riwayat/"

delete_output = 'SAVE_OUTPUT' not in os.environ
data_dir = templates_folder
# Get rid of the skewed scan with default parameters
with aspycore.as_of(Image.load(os.path.join(data_dir, "image_2454076420-20-53-06.jpg")), RasterImage) as image:
	image.normalize_angle(False, Color.light_gray)
	image.save(os.path.join(data_dir, "result.jpg"))

# if delete_output:
# 	os.remove(os.path.join(data_dir, "result.jpg"))
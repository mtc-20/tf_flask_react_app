import io
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import collections
from PIL import Image, ImageDraw, ImageFont
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import get_file
from tensorflow.saved_model import load
from time import perf_counter
import tarfile

STANDARD_COLORS = [
		'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
		'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
		'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
		'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
		'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
		'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
		'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
		'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
		'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
		'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
		'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
		'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
		'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
		'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
		'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
		'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
		'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
		'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
		'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
		'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
		'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
		'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
		'WhiteSmoke', 'Yellow', 'YellowGreen'
]

def draw_bbox_on_arr(img, ymin, xmin, ymax, xmax, color='red', thickness=2, display_str_list=(), use_normalized_coords=True):
	img_pil = Image.fromarray(np.uint8(img)).convert('RGB')
	draw_bbox_on_img(img_pil, ymin, xmin, ymax, xmax, color, thickness, display_str_list, use_normalized_coords)
	np.copyto(img, np.array(img_pil))

def draw_bbox_on_img(img, ymin, xmin, ymax, xmax, color='red', thickness=2, display_str_list=(), use_normalized_coords=True):
	draw = ImageDraw.Draw(img)
	im_w, im_h = img.size
	if use_normalized_coords:
		(left, right, top, bottom) = (xmin*im_w, xmax*im_w, ymin*im_h, ymax*im_h)
	else:
		(left, right, top, bottom) = (xmin, xmax, ymin, ymax)
	if thickness>0:
		draw.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)], width=thickness, fill=color)

	try:
		font = ImageFont.truetype('arial.ttf', 24)
	except IOError:
		font = ImageFont.load_default()

	display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
	total_display_str_height = (1 + 2*0.05)*sum(display_str_heights)

	if top > total_display_str_height:
		text_bottom = top
	else:
		text_bottom = bottom + total_display_str_height
	for display_str in display_str_list[::-1]:
		text_w, text_h = font.getsize(display_str)
		margin = np.ceil(0.05*text_h)
		draw.rectangle([(left, text_bottom - text_h -2*margin), (left+text_w, text_bottom)])
		draw.text((left+margin, text_bottom-text_h-margin), display_str, fill='black', font=font)
		text_bottom -= text_h - 2*margin


def viz_boxes_and_labels_on_arr(img, boxes, classes, scores, labels_dict, use_normalized_coords=True, max_boxes_to_draw=30, min_score_thresh=0.4):
	box_to_display_str_map = collections.defaultdict(list)
	box_to_color_map = collections.defaultdict(str)

	if not max_boxes_to_draw:
		max_boxes_to_draw = boxes.shape[0]
		
	for i in range(boxes.shape[0]):
		if max_boxes_to_draw == len(box_to_color_map):
			break
		if scores is None or scores[i] > min_score_thresh:
			box = tuple(boxes[i].tolist())
			if scores is None:
				box_to_color_map = 'black'
			else:
				display_str = ''
				if classes[i] in labels_dict:
						class_name = labels_dict[classes[i]]
				else:
						class_name ='N/A'
				display_str = str(class_name)

				if not display_str:
						display_str = "{}%".format(round(100*scores[i]))
				else:
						display_str = "{}:{}%".format(display_str, round(100*scores[i]))
				box_to_display_str_map[box].append(display_str)

				box_to_color_map[box] = STANDARD_COLORS[classes[i]%len(STANDARD_COLORS)]

	
	for box, color in box_to_color_map.items():
		ymin, xmin, ymax, xmax = box
		draw_bbox_on_arr(img, ymin, xmin, ymax, xmax, color=color, thickness=4, display_str_list=box_to_display_str_map[box], use_normalized_coords=use_normalized_coords)
	return img


def read_label_map(label_map_path:str):
	"""Read COCO labelmap.pbtxt and convert to dict

	Args:
			label_map_path (str): path to labelmap proto

	Returns:
			items(dict): dictionary of the COCO classes as {index : label_name}
	"""
	item_id = None
	item_name = None
	items = {}

	with open(label_map_path, "r") as file:
		for line in file:
			line.replace(" ", "")
			if line == "item{":
				pass
			elif line == "}":
				pass
			elif "id" in line:
				item_id = int(line.split(":", 1)[1].strip())
			elif "display_name" in line:
				item_name = line.split(" ")[-1].replace("\"", " ").strip()
			if item_id is not None and item_name is not None:
				items[item_id] = item_name
				item_id = None
				item_name = None

	return items



MODEL_NAME = "/app/backend/ssd_mobilenet_v2"
model_url = "https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2?tf-hub-format=compressed"
model_path = get_file("/app/backend/ssd_mobilenet_v2.tar.gz", model_url)

# print(model_path)

assert os.path.exists("/app/backend/ssd_mobilenet_v2.tar.gz"), "File not downloaded"
with tarfile.open("/app/backend/ssd_mobilenet_v2.tar.gz", "r:gz") as tar:
	tar.extractall(MODEL_NAME)



labels_path = get_file(
'mscoco_label_map.pbtxt','https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/mscoco_label_map.pbtxt')
print(labels_path)

labels_dict = read_label_map(labels_path)

start = perf_counter()
model = load(MODEL_NAME)
elapsed = perf_counter() - start
print("Time to load model: {} sec".format(elapsed))


def getDetections(image_file, model):
	img_input = Image.open(image_file)
	img_input = img_input.convert('RGB')
	im_w, im_h = img_input.size
	img_arr = image.img_to_array(img_input)
	img_arr = img_arr.reshape(1,im_h,im_w,3)
	# start = perf_counter()
	out_base = model(img_arr)
	# elapsed = perf_counter() - start
	# print("Time for inference: {} sec".format(elapsed))
	out_base['detection_classes'] = out_base['detection_classes'].numpy().astype(np.int64)

	img_numpy = img_arr.astype(np.uint8).copy()
	overlaid = viz_boxes_and_labels_on_arr(img_numpy[0], out_base['detection_boxes'].numpy()[0], out_base['detection_classes'][0], out_base['detection_scores'].numpy()[0], labels_dict, max_boxes_to_draw=20, min_score_thresh=.6, use_normalized_coords=True)
	return overlaid

def overlayImage(image_file):
	overlay_arr = getDetections(image_file, model)
	overlay_img = Image.fromarray(overlay_arr.astype(np.uint8))
	file_obj = io.BytesIO()
	overlay_img.save(file_obj, 'PNG')
	file_obj.seek(0)
	return file_obj

	


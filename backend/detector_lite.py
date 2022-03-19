from io import BytesIO
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import get_file
from tensorflow import lite
from tensorflow import convert_to_tensor
from time import perf_counter
import gc


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

def draw_bbox_on_img(img, ymin, xmin, ymax, xmax, color='red', thickness=2, display_str_list=()):
		draw = ImageDraw.Draw(img)
		im_w, im_h = img.size
		(left, right, top, bottom) = (xmin*im_w, xmax*im_w, ymin*im_h, ymax*im_h)
		if thickness > 0:
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
		# plt.imshow(img)
		return img

def viz_bboxes_and_labels(img, boxes, labels, scores, labels_dict, max_boxes_to_draw=20, min_score_thresh=0.3):
		box_to_display_str_map = defaultdict(list)
		box_to_color_map = defaultdict(str)

		if not max_boxes_to_draw:
				max_boxes_to_draw=boxes.shape[0]
		for i in range(boxes.shape[0]):
				if max_boxes_to_draw == len(box_to_color_map):
						break

				if scores is None or scores[i] > min_score_thresh:
						box = tuple(boxes[i].tolist())
						if scores is None:
								box_to_color_map[box] = 'black'
						else:
								display_str = ''
								if labels[i] in labels_dict:
										class_name = labels_dict[labels[i]]
								else:
										class_name = "N/A"
								display_str = str(class_name)

								if not display_str:
										display_str = "{}%".format(round(100*scores[i]))
								else:
										display_str = "{}:{}%".format(display_str, round(100*scores[i]))
								box_to_display_str_map[box].append(display_str)

								box_to_color_map[box] = STANDARD_COLORS[labels[i]%len(STANDARD_COLORS)]

		img = img.convert('RGB')
		for box, color in box_to_color_map.items():
				ymin, xmin, ymax, xmax = box
				draw_bbox_on_img(img, ymin, xmin, ymax, xmax, color=color, thickness=4, display_str_list=box_to_display_str_map[box])
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




## TFLite model
model_url = "https://tfhub.dev/tensorflow/lite-model/efficientdet/lite3/detection/default/1?lite-format=tflite"
MODEL_NAME = "efficientdet_lite3_default.tflite"
model_path = get_file(MODEL_NAME, model_url)
assert os.path.exists(model_path), "File not downloaded"

labels_path = get_file(
'mscoco_label_map.pbtxt','https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/mscoco_label_map.pbtxt')
print(labels_path)

labels_dict = read_label_map(labels_path)

start = perf_counter()
interpreter = lite.Interpreter(model_path)
elapsed = perf_counter() - start
print("Time to load model: {} sec".format(elapsed))

interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
w, h = input_details[0]['shape'][1:3]
output_details = interpreter.get_output_details()


def getDetections(image_file, interpreter, input_details):
	img_input = Image.open(image_file)
	img_input = img_input.convert('RGB')
	img_input = img_input.resize((w,h), Image.NEAREST)
	# im_w, im_h = img_input.size
	img_arr = image.img_to_array(img_input)
	input_data = np.expand_dims(img_arr, axis=0)

	# start = perf_counter()
	# img_tensor = convert_to_tensor(input_data, np.uint8)
	interpreter.set_tensor(input_details[0]['index'], input_data)
	interpreter.invoke()
	
	# elapsed = perf_counter() - start
	# print("Time for inference: {} sec".format(elapsed))
	boxes = interpreter.get_tensor(output_details[0]['index'])[0]
	labels = interpreter.get_tensor(output_details[1]['index'])[0]
	scores = interpreter.get_tensor(output_details[2]['index'])[0]
	num = interpreter.get_tensor(output_details[3]['index'])[0]

	overlaid = viz_bboxes_and_labels(img_input, boxes.copy(), labels.astype(np.int64).copy(), scores.copy(), labels_dict)
	del img_arr
	gc.collect()
	return overlaid

def overlayImage(image_file):

	# interpreter = lite.Interpreter(model_path)
	overlay_img = getDetections(image_file, interpreter)
	# overlay_img = Image.fromarray(overlay_arr.astype(np.uint8))
	file_obj = BytesIO()
	overlay_img.save(file_obj, 'PNG')
	file_obj.seek(0)
	return file_obj

	


import torch
import numpy as np
from PIL import Image
from stegano_model.steg_net import StegNet
from skimage.io import imsave, imread


def load_model(path_model):
    """Loads the pytorch model
    Input:
        path_model: path to the model
    Output:
        model: pytorch model
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = StegNet()
    model.load_state_dict(
    torch.load(path_model, map_location={'cuda:0': 'cpu'}))  # Choose whatever GPU device number you want
    model.to(device)
    return model


def open_image_and_resize(image, width, height):
    """Open an image and resize it
    Input:
        image: path to the image
        width: width of the image
        height: height of the image
    Output:
        image_resized: resized image
    """
    im = Image.open(image)
    newsize = (width, height)
    image_resized = im.resize(newsize)
    return image_resized


def image_to_tensor(path_image, convert="RGB", device="cpu"):
    """Converts an image to a tensor
    Input:
        path_image: path to the image
        convert: RGB or L
        device: cpu or cuda
    Output:
        image_array: tensor of the image
    """
    image_array = np.array(open_image_and_resize(path_image, 64, 64).convert(convert)).astype(np.uint8)
    return torch.from_numpy(image_array).float().to(device)


def images_to_tensor(path_source, path_payload, device='cpu'):
    """Converts two images to tensors
    Input:
        path_source: path to the source image
        path_payload: path to the payload image
        device: cpu or cuda
    Output:
        image_source_tensor: tensor of the source image
        image_payload_tensor: tensor of the payload image
    """
    image_source_tensor = image_to_tensor(path_source, convert="RGB", device=device)
    image_payload_tensor = image_to_tensor(path_payload, convert="L", device=device)

    return image_source_tensor, image_payload_tensor


def inference_encoder(model, source_img, Payload_img, size_image=64, device='cpu'):
    """Encodes the payload image into the source image
    Input:
        model: pytorch model
        source_img: path to the source image
        Payload_img: path to the payload image
        size_image: size of the image
        device: cpu or cuda
    Output:
        path_im_encoded: path to the encoded image
        numpy_tensor_encoded: tensor of the encoded image
    """
    im_source, im_payload = images_to_tensor(source_img, Payload_img, device=device)
    with torch.no_grad():
        model.eval()
        encoded_image = model.predict_encoder(im_source, im_payload) 

    encoded_image = encoded_image.cpu()
    numpy_tensor_encoded = encoded_image.view((-1, size_image, size_image, 3)).numpy()[0]

    path_im_encoded = 'results/image_encoded_result.tiff'
    imsave(path_im_encoded, numpy_tensor_encoded/255)

    return path_im_encoded, numpy_tensor_encoded/255


def inference_decoder(model, image_to_decode, size_image=64, device='cpu'):
    """Decodes the payload image from the source image
    Input:
        model: pytorch model
        image_to_decode: path to the image to decode
        size_image: size of the image
        device: cpu or cuda
    Output:
        path_im_decoded: path to the decoded image
        decoded_payload_result: tensor of the decoded image
    """
    image_to_decode = imread(image_to_decode)
    image_to_decode = image_to_decode.astype(np.float32)*255
    image_to_decode_tensor = torch.from_numpy(image_to_decode).float().to(device)

    with torch.no_grad():
        model.eval()
        decoded_payload = model.predict_decoder(image_to_decode_tensor)

    decoded_payload = decoded_payload.cpu()
    decoded_payload_result = decoded_payload.view((-1, size_image, size_image)).numpy()[0].astype('uint8')

    path_im_decoded = 'results/image_decoded_result.png'
    imsave(path_im_decoded, decoded_payload_result)

    return path_im_decoded, decoded_payload_result

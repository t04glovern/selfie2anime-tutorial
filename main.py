import argparse
import threading
import time
import base64
from flask import Flask, request, jsonify

from UGATIT import UGATIT
from utils import *

class State:
    # Device ID (typically 0)
    video_device_id = 0
    # can alternatively be a RTSP endpoint
    # video_device_id = 'http://192.168.0.1:8080/video/mjpeg'

    # Local render scale factor.
    display_scale = 3

    # Current frame.
    frame = None

    # When changed to false, program will be terminated.
    running = True

# Init state for camera
state = State()

# Flask app
app = Flask(__name__)

# Global ref for GAN
gan_ref = None

"""parsing and configuration"""
def parse_args():
    desc = "Tensorflow implementation of U-GAT-IT"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--phase', type=str, default='train', help='[train / test]')
    parser.add_argument('--light', type=str2bool, default=False, help='[U-GAT-IT full version / U-GAT-IT light version]')
    parser.add_argument('--dataset', type=str, default='selfie2anime', help='dataset_name')

    parser.add_argument('--epoch', type=int, default=100, help='The number of epochs to run')
    parser.add_argument('--iteration', type=int, default=10000, help='The number of training iterations')
    parser.add_argument('--batch_size', type=int, default=1, help='The size of batch size')
    parser.add_argument('--print_freq', type=int, default=1000, help='The number of image_print_freq')
    parser.add_argument('--save_freq', type=int, default=1000, help='The number of ckpt_save_freq')
    parser.add_argument('--decay_flag', type=str2bool, default=True, help='The decay_flag')
    parser.add_argument('--decay_epoch', type=int, default=50, help='decay epoch')

    parser.add_argument('--lr', type=float, default=0.0001, help='The learning rate')
    parser.add_argument('--GP_ld', type=int, default=10, help='The gradient penalty lambda')
    parser.add_argument('--adv_weight', type=int, default=1, help='Weight about GAN')
    parser.add_argument('--cycle_weight', type=int, default=10, help='Weight about Cycle')
    parser.add_argument('--identity_weight', type=int, default=10, help='Weight about Identity')
    parser.add_argument('--cam_weight', type=int, default=1000, help='Weight about CAM')
    parser.add_argument('--gan_type', type=str, default='lsgan', help='[gan / lsgan / wgan-gp / wgan-lp / dragan / hinge]')

    parser.add_argument('--smoothing', type=str2bool, default=True, help='AdaLIN smoothing effect')

    parser.add_argument('--ch', type=int, default=64, help='base channel number per layer')
    parser.add_argument('--n_res', type=int, default=4, help='The number of resblock')
    parser.add_argument('--n_dis', type=int, default=6, help='The number of discriminator layer')
    parser.add_argument('--n_critic', type=int, default=1, help='The number of critic')
    parser.add_argument('--sn', type=str2bool, default=True, help='using spectral norm')

    parser.add_argument('--img_size', type=int, default=256, help='The size of image')
    parser.add_argument('--img_ch', type=int, default=3, help='The size of image channel')
    parser.add_argument('--augment_flag', type=str2bool, default=True, help='Image augmentation use or not')

    parser.add_argument('--checkpoint_dir', type=str, default='checkpoint',
                        help='Directory name to save the checkpoints')
    parser.add_argument('--result_dir', type=str, default='results',
                        help='Directory name to save the generated images')
    parser.add_argument('--log_dir', type=str, default='logs',
                        help='Directory name to save training logs')
    parser.add_argument('--sample_dir', type=str, default='samples',
                        help='Directory name to save the samples on training')

    return check_args(parser.parse_args())

"""checking arguments"""
def check_args(args):
    # --checkpoint_dir
    check_folder(args.checkpoint_dir)

    # --result_dir
    check_folder(args.result_dir)

    # --result_dir
    check_folder(args.log_dir)

    # --sample_dir
    check_folder(args.sample_dir)

    # --epoch
    try:
        assert args.epoch >= 1
    except:
        print('number of epochs must be larger than or equal to one')

    # --batch_size
    try:
        assert args.batch_size >= 1
    except:
        print('batch size must be larger than or equal to one')
    return args

"""read frame from camera"""
def read_frame_thread():
    try:
        capture = cv2.VideoCapture(state.video_device_id)
        while state.running:
            _, frame = capture.read()
            state.frame = frame
            time.sleep(0.01)

    except Exception as e:
        print(e)
        state.running = False

"""process any key presses"""
def process_events():
    if cv2.waitKey(1) & 0xff == 27:
        state.running = False

"""video stream"""
def video(args):
    # open session
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
        gan = UGATIT(sess, args)

        # build graph
        gan.build_model()

        # show network architecture
        show_all_variables()

        # load model for use in video stream
        gan.video_inference_init()

        # Run frame thread
        threading.Thread(target=read_frame_thread).start()

        while state.running:
            if state.frame is None:
                time.sleep(0.01)
                continue

            # Get recent frame
            frame = state.frame

            # generate image
            gen_image = gan.video_inference(frame)

            # display frame
            cv2.imshow('frame', cv2.resize(gen_image, None, fx=state.display_scale, fy=state.display_scale))

            # handle key press events
            process_events()

"""request endpoint"""
@app.route('/process', methods=['POST'])
def process():
    _, encoded = request.json['image'].split(",", 1)
    image_bytes = base64.b64decode(encoded)

    #  convert binary data to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    #  let opencv decode image to correct format
    img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

    # generate image
    global gan_ref
    gen_image = gan_ref.video_inference(img)

    _, buffer = cv2.imencode('.jpg', gen_image)
    buffer_text = base64.b64encode(buffer)

    return jsonify(
        selfie=str(buffer_text)
    )

"""request endpoint"""
@app.route('/health', methods=['GET'])
def health():
    return jsonify(
        status=200
    )

"""main"""
def main():
    # parse arguments
    args = parse_args()

    if args is None:
        exit()

    if args.phase == 'video':
        video(args)

    # open session
    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True)) as sess:
        gan = UGATIT(sess, args)

        # build graph
        gan.build_model()

        # show network architecture
        show_all_variables()

        if args.phase == 'web':
            gan.video_inference_init()

            global gan_ref
            gan_ref = gan

            app.run(host="0.0.0.0", port=5000)
            exit()

        if args.phase == 'train':
            gan.train()
            print(" [*] Training finished!")

        if args.phase == 'test':
            gan.test()
            print(" [*] Test finished!")

if __name__ == '__main__':
    main()

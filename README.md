# Why background changer?

This project is mostly for learning dash/flask and mediapipe/opencv/paddleseg.

Segmentation and matting is done with [PaddleSegMatting](https://github.com/PaddlePaddle/PaddleSeg/tree/release/2.7/Matting) more specifically I used a PP-MattingV2
that is SOTA for image matting. The model is also lite and runs in about 0.5 seconds per photo.

The results are as good as most online removers or changers, and often even better.


# Preview

![Alt text](assets/demo.gif)


# Run
```bash

git clone https://github.com/filnow/bg-changer.git
cd bg-changer
pip install -r requirements.txt
python3 app.py

```

# TODO

* add video support
* make frontend kinda good
* import ppmatting from somewhere else

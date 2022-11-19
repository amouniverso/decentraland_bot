# decentraland_bot
python train.py --workers 1 --device 0 --batch-size 8 --epochs 100 --img 640 640 --data data/custom_data.yaml --hyp data/hyp.scratch.custom.yaml --cfg cfg/training/yolov7-custom.yaml --name yolov7-wondermine_meteor --weights yolov7.pt  

python detect.py --weights yolov7_custom.pt --conf 0.3 --img-size 640 --source meteor.mp4 --view-img --no-trace
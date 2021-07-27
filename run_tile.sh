python run_infer.py \
--gpu='1' \
--nr_types=5 \
--type_info_path=type_info.json \
--batch_size=1 \
--model_mode=original \
--model_path="/data/hovernet_training_data/tabsap/logs/01/net_epoch=50.tar" \
--nr_inference_workers=4 \
--nr_post_proc_workers=4 \
tile \
--input_dir="/data/tabsap/test/images/" \
--output_dir="/data/tabsap/test/pred_images/" \
--mem_usage=0.1 \
--draw_dot \
--save_raw_map

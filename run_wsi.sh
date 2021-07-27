python run_infer.py \
--gpu='0,1' \
--nr_types=5 \
--type_info_path=type_info.json \
--batch_size=1 \
--model_mode=fast \
--model_path="/data/hovernet_training_data/tabsap/logs/01/net_epoch=50.tar" \
--nr_inference_workers=8 \
--nr_post_proc_workers=16 \
wsi \
--input_dir=dataset/sample_wsis/wsi/ \
--output_dir=dataset/sample_wsis/out/ \
--input_mask_dir=dataset/sample_wsis/msk/ \
--save_thumb \
--save_mask
